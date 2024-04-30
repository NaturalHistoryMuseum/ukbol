from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    response = client.get("/api/status")
    assert response.is_json
    assert response.json == {
        "status": ":)",
        "db": {"specimen": 1000, "synonym": 4, "taxon": 16},
    }
