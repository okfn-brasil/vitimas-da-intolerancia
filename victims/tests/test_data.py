import asyncio
from datetime import date
from pathlib import Path

from victims.data import Data, round_robin


FIXTURES = (
    Path() / "victims" / "tests" / "fixtures" / "cases.csv",
    Path() / "victims" / "tests" / "fixtures" / "stories.csv",
)


async def mocked_responses(_self):
    with open(FIXTURES[0], "rb") as cases, open(FIXTURES[1], "rb") as stories:
        return (cases.read(), stories.read())


def test_round_robin():
    assert tuple(round_robin("ABC", "D", "EF")) == ("A", "D", "E", "B", "F", "C")


def test_data_cases_property(mocker):
    mocker.patch.object(Data, "fetch_spreadsheets", new=mocked_responses)

    data = Data()
    loop = asyncio.get_event_loop()
    cases = loop.run_until_complete(data.cases())

    assert len(cases) == 5
    cases[0].when == date(2018, 10, 8)
    cases[-1].when == date(2018, 10, 3)
