from datetime import datetime

from ukbol.extensions import db


def log(message: str):
    print(f"[{datetime.now().isoformat(sep=' ')}] {message}")


def create_all_tables():
    db.create_all()


def drop_all_tables():
    db.drop_all()
