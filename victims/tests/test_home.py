from datetime import date

from victims.data import Data
from victims.models import Case, Story


async def mocked_cases(_self):
    story = Story(
        url="https://florianopol.is/",
        source="DC",
        title="Foo Bar",
        image_or_video="https://florianopol.is/cover.png",
        summary="Foo, bar!",
        case_id=42,
    )
    case = Case(
        id=42,
        when=date(2018, 10, 7),
        state="SC",
        city="Florianópolis",
        tags=["homicídio", "mulher", "tag que não existe"],
        stories=[story],
        aggressor_side="E",
    )
    return (case,)


def test_home_status(client, mocker):
    mocker.patch.object(Data, "cases", new=mocked_cases)
    assert client.get("/").status_code == 200


def test_home_contents(client, mocker):
    mocker.patch.object(Data, "cases", new=mocked_cases)
    contents = client.get("/").data.decode("utf-8")
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
        "red",
        "mulher",
        "purple",
        "tag que não existe",
        "grey",
    )
    for expected in expected_terms:
        assert expected in contents
