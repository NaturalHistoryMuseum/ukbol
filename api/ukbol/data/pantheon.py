import csv
import os
import sys
from io import TextIOWrapper
from itertools import batched
from pathlib import Path
from typing import Iterable

from ukbol.data.utils import update_status
from ukbol.extensions import db
from ukbol.model import PantheonSpecies
from ukbol.utils import log


def iter_records(rows: Iterable[dict[str, str]]) -> Iterable[PantheonSpecies]:
    """
    Given an iterable of rows from the PANTHEON csv snapshot as dicts, return an
    iterable of PantheonSpecies objects created from them.

    :param rows: the rows as dicts
    :return: an iterable of PantheonSpecies objects
    """
    for row in rows:
        yield PantheonSpecies(
            **{
                # convert field names to lowercase with underscores instead of spaces to
                # match our table model, and convert empty str values into Nones
                field.replace(" ", "_").lower(): value if value.strip() else None
                for field, value in row.items()
            }
        )


def rebuild_pantheon_tables(pantheon_snapshot: Path):
    """
    Given the path to a PANTHEON CSV snapshot, read the file and replace the current
    data in the PantheonSpecies table with the data. All old data is deleted.

    :param pantheon_snapshot: Path to the PANTHEON CSV snapshot
    """
    log("Removing existing data...")
    PantheonSpecies.query.delete()
    db.session.commit()

    # increase the field size limit to avoid errors when reading the PANTHEON csv
    csv.field_size_limit(sys.maxsize)

    with pantheon_snapshot.open("rb") as f:
        text_csv = TextIOWrapper(f, encoding="utf-8", newline="")
        reader: Iterable[dict] = csv.DictReader(text_csv, dialect=csv.excel)

        log("Loading data into database...")
        count = 0
        for batch in batched(iter_records(reader), 1000):
            db.session.add_all(batch)
            db.session.commit()
            count += len(batch)
            if count % 1000 == 0:
                log(f"{count} so far...")

    version = os.environ.get("UKBOL_PANTHEON_DATA_VERSION", None)
    species_count = PantheonSpecies.query.count()
    update_status("pantheon-species", species_count, version)
    log(f"Added {species_count} pantheon species")
