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


def clamp(value: int, minimum: int, maximum: int) -> int:
    """
    Clamps the given value between the minimum and maximum values.

    :param value: the value to clamp
    :param minimum: the minimum allowed value
    :param maximum: the maximum allow value
    :return: the clamped value
    """
    return max(min(value, maximum), minimum)
