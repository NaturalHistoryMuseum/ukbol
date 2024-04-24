import csv
import sys
import tarfile
from io import TextIOWrapper
from itertools import batched
from pathlib import Path
from typing import Iterable

from ukbol.extensions import db
from ukbol.model import Specimen
from ukbol.utils import log


def get_tsv_name(tar: tarfile.TarFile) -> str:
    for name in tar.getnames():
        if name.endswith(".tsv"):
            return name
    raise Exception("Could not find .tsv file in BOLD data package")


def get(row: dict[str, str], column: str, lowercase: bool = False) -> str | None:
    value = row.get(column, None)
    if value and value != "None":
        return value.lower() if lowercase else value
    return None


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
    data = {}
    for rank in order:
        name = get(row, rank, lowercase=True)
        data[rank] = name
        if name:
            data["name"] = name
            data["rank"] = rank
    data["cls"] = data.pop("class")
    return data


def iter_specimens(rows: Iterable[dict[str, str]]) -> Iterable[Specimen]:
    yield from (
        Specimen(
            specimen_id=get(row, "specimenid"),
            bin_uri=get(row, "bin_uri"),
            country=get(row, "country", lowercase=True),
            **extract_taxonomy(row),
        )
        for row in rows
    )


def rebuild_bold_tables(bold_snapshot: Path):
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
