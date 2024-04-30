from flask import Flask

from ukbol.routes import status
from ukbol.routes.api import bind_api_routes


def bind_routes(app: Flask):
    app.register_blueprint(status.blueprint)
    bind_api_routes(app)
