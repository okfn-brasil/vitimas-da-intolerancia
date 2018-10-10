from datetime import date
from unittest.mock import PropertyMock

from victims import app
from victims.data import Data
from victims.models import Case, Story


STORY = Story(
    url="https://florianopol.is/",
    source="DC",
    title="Foo Bar",
    image_or_video="https://florianopol.is/cover.png",
    summary="Foo, bar!",
    case_id=42,
)
CASE = Case(
    id=42,
    when=date(2018, 10, 7),
    state="SC",
    city="Florianópolis",
    tags=["homicídio", "mulher"],
    stories=[STORY],
)
CASES = [CASE]


def test_home_status(mocker):
    cases = mocker.patch.object(Data, "cases", new_callable=PropertyMock)
    cases.return_value = CASES
    _, response = app.test_client.get("/")
    assert response.status == 200


def test_home_contents(mocker):
    cases = mocker.patch.object(Data, "cases", new_callable=PropertyMock)
    cases.return_value = CASES
    _, response = app.test_client.get("/")
    expected_terms = (
        "#VítimasDaIntolerância",
        "https://florianopol.is/",
        "DC",
        "Foo Bar",
        "https://florianopol.is/cover.png",
        "Foo, bar!",
        "SC",
        "Florianópolis",
        "homicídio",
        "mulher",
    )
    for expected in expected_terms:
        assert expected in response.text
