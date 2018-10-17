from victims import app


def test_map_status(mocker):
    _, response = app.test_client.get("/map.html")
    assert response.status == 200


def test_map_contents():
    _, response = app.test_client.get("/map.html")
    assert "Mapa Interativo" in response.text
