from datetime import datetime, timezone

from ukbol.extensions import db
from ukbol.model import DataSourceStatus


def get(
    row: dict[str, str],
    column: str,
    lowercase: bool = False,
    filter_str_nones: bool = False,
) -> str | None:
    """
    Given a row of data as a dict, return the value of the given column or None if the
    column isn't present or the column's value is the string "None".

    :param row: the row as a dict
    :param column: the column to get the value of
    :param lowercase: whether to lowercase value or not, defaults to False
    :param filter_str_nones: whether to filter out "None" values or not which is how
                             missing data is represented in BOLD TSVs, defaults to False
    :return: the value or None
    """
    value = row.get(column, None)
    if value and (not filter_str_nones or value != "None"):
        return value.lower() if lowercase else value
    return None


def update_status(name: str, total: int, version: str | None = None):
    updated_at = datetime.now(timezone.utc)
    status = DataSourceStatus.get(name)
    if status is None:
        db.session.add(
            DataSourceStatus(
                name=name, updated_at=updated_at, version=version, total=total
            )
        )
    else:
        status.updated_at = updated_at
        status.version = version
        status.total = total
    db.session.commit()
