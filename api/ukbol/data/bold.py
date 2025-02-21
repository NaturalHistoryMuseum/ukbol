import csv
import sys
import tarfile
from io import TextIOWrapper
from itertools import batched
from pathlib import Path
from typing import Iterable

from ukbol.data.utils import get
from ukbol.extensions import db
from ukbol.model import Specimen
from ukbol.utils import log


def get_tsv_name(tar: tarfile.TarFile) -> str:
    """
    Given a path to a tar.gz archive, return the name of the first TSV file inside it
    that we encounter. The BOLD tar.gz snapshots only have a single JSON and a single
    TSV file within them currently so this should be able to find the TSV file we need
    to read without knowing what it is called.

    If no TSV file can be found, an Exception is raised.

    :param tar: the Path to the tar.gz BOLD snapshot
    :return: the name of the TSV file
    """
    for name in tar.getnames():
        if name.endswith(".tsv"):
            return name
    raise Exception("Could not find .tsv file in BOLD data package")


# taxonomic rank order
order = (
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "subfamily",
    "genus",
    "species",
    "subspecies",
)


def extract_taxonomy(row: dict[str, str]) -> dict[str, str | None]:
    """
    Given a row of data from a BOLD snapshot, return a dict which can be used to
    populate a Specimen object. Any taxonomic ranks found will be present in the
    returned dict (with the values lowercased) along with the "name" and "rank" keys
    indicating the most precise rank present in the row.

    :param row: the row as a dict
    :return: the found taxonomy columns as a dict
    """
    data = {}
    for rank in order:
        name = get(row, rank, lowercase=True, filter_str_nones=True)
        if name:
            # add the rank and name to the data and update the lowest name and rank
            # we've found so far
            data[rank] = name
            data["name"] = name
            data["rank"] = rank
    # in the data model, the "class" column is called "cls" because class is a Python
    # keyword and therefore not usable
    if "class" in data:
        data["cls"] = data.pop("class")
    return data


def iter_specimens(rows: Iterable[dict[str, str]]) -> Iterable[Specimen]:
    """
    Given an iterable of rows from the BOLD snapshot as dicts, return an iterable of
    Specimen objects created from them.

    :param rows: the rows as dicts
    :return: an iterable of Specimen objects
    """
    yield from (
        Specimen(
            specimen_id=get(row, "specimenid", filter_str_nones=True),
            bin_uri=get(row, "bin_uri", filter_str_nones=True),
            country=get(row, "country_iso", lowercase=True, filter_str_nones=True),
            **extract_taxonomy(row),
        )
        for row in rows
    )


def rebuild_bold_tables(bold_snapshot: Path):
    """
    Given the path to a BOLD snapshot, read the TSV in that snapshot and replace the
    current data in the Specimen table with the data. All old data is deleted.

    :param bold_snapshot: Path to the BOLD snapshot
    """
    log("Removing existing data...")
    Specimen.query.delete()
    db.session.commit()

    # increase the field size limit to avoid errors when reading the BOLD tsv
    csv.field_size_limit(sys.maxsize)

    log("Reading tsv from zip, this may take a bit of time...")
    with tarfile.open(bold_snapshot) as tar:
        tsv_file_name = get_tsv_name(tar)
        raw_tsv = tar.extractfile(tsv_file_name)
        text_tsv = TextIOWrapper(raw_tsv, encoding="utf-8", newline="")
        reader: Iterable[dict] = csv.DictReader(text_tsv, dialect=csv.excel_tab)

        log("Loading data into database...")
        count = 0
        for batch in batched(iter_specimens(reader), 1000):
            db.session.add_all(batch)
            db.session.commit()
            count += len(batch)
            if count % 10000 == 0:
                log(f"{count} so far...")

    log(f"Added {Specimen.query.count()} specimens")
