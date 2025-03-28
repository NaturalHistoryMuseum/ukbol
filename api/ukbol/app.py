from flask import Flask

from ukbol.api import bind_api_routes
from ukbol.extensions import db, ma, migrate


def create_app() -> Flask:
    """
    Creates and returns the Flask application.

    :return: the Flask application object
    """
    app = Flask(__name__)

    # setup the config from env vars
    app.config.from_prefixed_env()
    app.config.from_prefixed_env("UKBOL")

    # setup extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # import models so that they get noticed by sqlalchemy and alembic

    # setup routes
    bind_api_routes(app)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
