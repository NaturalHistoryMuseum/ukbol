from datetime import datetime

from ukbol.extensions import db


def log(message: str):
    """
    Logs a message to the console with a prefixed timestamp.

    :param message: the message to log
    """
    print(f"[{datetime.now().isoformat(sep=' ')}] {message}")


def create_all_tables():
    db.create_all()


def drop_all_tables():
    db.drop_all()
