from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

from tests.data.test_uksi import mock_nbn_records
from ukbol.app import create_app
from ukbol.data.bold import rebuild_bold_tables
from ukbol.data.uksi import rebuild_uksi_tables
from ukbol.extensions import db


@pytest.fixture
def app_no_data() -> Flask:
    app = create_app()

    with app.app_context():
        # drop everything and make it all again
        db.drop_all()
        db.create_all()

        yield app

        # drop it all to make sure we leave a clean state
        db.session.close()
        db.drop_all()


@pytest.fixture
def app(app_no_data) -> Flask:
    # load some uksi data
    with mock_nbn_records():
        rebuild_uksi_tables()

    # load some bold data
    bold_tar_gz = Path(__file__).parent / "files" / "BOLD_Public.19-Apr-2024.tar.gz"
    rebuild_bold_tables(bold_tar_gz)

    yield app_no_data


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def client_no_data(app_no_data: Flask) -> FlaskClient:
    return app_no_data.test_client()
