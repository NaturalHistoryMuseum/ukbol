from flask import Flask

from ukbol.routes.api import bind_api_routes


def bind_routes(app: Flask):
    bind_api_routes(app)
