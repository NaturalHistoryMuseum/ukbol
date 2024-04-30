from flask import Blueprint

from ukbol.model import Specimen, Synonym, Taxon

blueprint = Blueprint("status", __name__)


@blueprint.get("/status")
def status() -> dict:
    """
    Returns a status response to simply show that things are alive. This includes some
    basic counts from the database, which will in turn therefore provide a status on the
    database's health, and provide information about the health of the data in the
    database.

    :return: a dict as JSON
    """
    return {
        "status": ":)",
        "db": {
            "specimen": Specimen.query.count(),
            "taxon": Taxon.query.count(),
            "synonym": Synonym.query.count(),
        },
    }
