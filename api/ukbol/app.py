from flask import Flask

from ukbol.extensions import db, migrate
from ukbol.routes import bind_routes


def create_app() -> Flask:
    app = Flask(__name__)

    # setup the config from env vars
    app.config.from_prefixed_env()
    app.config.from_prefixed_env("UKBOL")

    # setup extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # setup routes
    bind_routes(app)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
