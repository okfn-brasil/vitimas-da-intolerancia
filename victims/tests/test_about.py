from victims import app


def test_about_status():
    _, response = app.test_client.get("/about.html")
    assert response.status == 200


def test_about_contents():
    _, response = app.test_client.get("/about.html")
    assert "Sobre o #VítimasDaIntolerância" in response.text
