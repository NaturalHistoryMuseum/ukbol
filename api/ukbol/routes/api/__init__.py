from flask import Flask

from ukbol.routes.api import taxon


def bind_api_routes(app: Flask):
    app.register_blueprint(taxon.blueprint, url_prefix="/api")
