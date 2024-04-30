from flask import Blueprint

blueprint = Blueprint("status", __name__)


@blueprint.route("/status")
def status() -> dict:
    return {"status": ":)"}
