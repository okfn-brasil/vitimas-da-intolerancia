def test_about_status(client):
    assert client.get("/about.html").status_code == 200


def test_about_contents(client):
    contents = client.get("/about.html").data.decode("utf-8")
    assert "Sobre o #VítimasDaIntolerância" in contents
