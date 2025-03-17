from flask.testing import FlaskClient


def test_status(client: FlaskClient):
    response = client.get("/api/status")
    assert response.is_json
    status = response.json
    assert status["status"] == ":)"
    sources = status["sources"]
    assert len(sources) == 4
    assert sources[0]["name"] == "bold-specimens"
    assert sources[0]["total"] == 999
    assert sources[1]["name"] == "pantheon-species"
    assert sources[1]["total"] == 11779
    assert sources[2]["name"] == "uksi-synonym"
    assert sources[2]["total"] == 4
    assert sources[3]["name"] == "uksi-taxa"
    assert sources[3]["total"] == 14
