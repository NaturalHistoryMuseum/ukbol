import csv
import sys
import tarfile
from io import TextIOWrapper
from itertools import batched
from pathlib import Path

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
        reader = csv.reader(
            text_tsv,
            # it's a tsv file
            dialect=csv.excel_tab,
            # nothing is double-quoted but there is at least one entry in a dump I have
            # seen where there is a single double quote as a value which breaks
            # everything if it's handled in the default fashion. Single-quotes are used
            # but only in string array values so we can safely allow the reader to
            # ignore them too
            quoting=csv.QUOTE_NONE,
        )

        # some fields in the source tsv have different names in the database, mainly
        # because they're invalid as python or postgresql names
        mapping = {
            "class": "cls",
            "country/ocean": "country_ocean",
            "province/state": "province_state",
        }
        # take the order of the tsv's fields, but replace the names we've changed
        columns = [mapping.get(field, field) for field in next(reader)]
        # double-check the columns we're going to use are actually in the database model
        for column in columns:
            assert column in Specimen.__table__.columns, "TSV fields must match model"

        # quote the column names for the copy sql
        col_str = ", ".join(f'"{column}"' for column in columns)
        copy_sql = f"COPY {Specimen.__table__.name} ({col_str}) FROM STDIN"

        # we lowercase the identification and rank on ingest for matching purposes
        to_lower = (
            columns.index("identification"),
            columns.index("identification_rank"),
        )

        try:
            # need a raw connection so that we can use a psycopg cursor for the copy
            raw_connection = db.engine.raw_connection()
            log("Loading data into database...")
            count = 0
            batch_size = 100_000
            # use copy to get the data in efficiently, but do it in transactions of
            # 100,000 records instead of one massive transaction to avoid a getting a
            # massive hang at the end
            for batch in batched(reader, batch_size):
                with raw_connection.transaction():
                    with raw_connection.cursor() as psycopg_cursor:
                        with psycopg_cursor.copy(copy_sql) as copy:
                            for row in batch:
                                # do some light value management, converting "None" and
                                # "" values to actual None values, plus lowercase a
                                # couple of columns
                                copy.write_row(
                                    [
                                        None
                                        if value == "None" or not value.strip()
                                        else value.lower()
                                        if i in to_lower
                                        else value
                                        for i, value in enumerate(row)
                                    ]
                                )
                            count += len(batch)
                log(f"{count} written so far...")
        finally:
            raw_connection.close()

    log(f"Added {Specimen.query.count()} specimens")
