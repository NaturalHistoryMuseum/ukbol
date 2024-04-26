import pytest
from flask import Flask

from ukbol.app import create_app
from ukbol.extensions import db
from ukbol.utils import create_all_tables, drop_all_tables


@pytest.fixture
def app() -> Flask:
    app = create_app()

    with app.app_context():
        # drop everything and make it all again
        db.drop_all()
        db.create_all()

        yield app

        # drop it all to make sure we leave a clean state
        db.session.close()
        db.drop_all()
