from flask import Blueprint

from ukbol.extensions import db
from ukbol.model import DataSourceStatus
from ukbol.schema import DataSourceStatusSchema

blueprint = Blueprint("status", __name__)

source_status_schema = DataSourceStatusSchema()


@blueprint.get("/status")
def status() -> dict:
    """
    Returns a status response to simply show that things are alive. This includes some
    basic counts from the database, which will in turn therefore provide a status on the
    database's health, and provide information about the health of the data in the
    database.

    :return: a dict as JSON
    """
    select = db.select(DataSourceStatus).order_by(DataSourceStatus.name)
    result = db.session.scalars(select)
    return {
        "status": ":)",
        "sources": source_status_schema.dump(result.all(), many=True),
    }
