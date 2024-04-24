from datetime import datetime

from ukbol.extensions import db


def log(message: str):
    print(f"[{datetime.now().isoformat(sep=' ')}] {message}")


def create_all_tables():
    from ukbol.model import Taxon, Specimen, Synonym

    db.create_all()
