from flask import Flask
from ukbol.routes import status


def bind_routes(app: Flask):
    app.register_blueprint(status.blueprint)
