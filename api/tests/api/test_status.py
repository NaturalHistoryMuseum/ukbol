from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    response = client.get("/api/status")
    assert response.is_json
    assert response.json == {
        "status": ":)",
        "db": {"specimen": 999, "synonym": 4, "taxon": 14, "pantheon": 11779},
    }
