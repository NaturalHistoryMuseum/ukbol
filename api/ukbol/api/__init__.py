from flask import Flask

from ukbol.api import taxon, status


def bind_api_routes(app: Flask):
    url_prefix = "/api"
    app.register_blueprint(status.blueprint, url_prefix=url_prefix)
    app.register_blueprint(taxon.blueprint, url_prefix=url_prefix)
