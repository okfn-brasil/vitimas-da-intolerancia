import asyncio
from datetime import date
from pathlib import Path

from victims.data import Data, round_robin


FIXTURES = Path() / "victims" / "tests" / "fixtures"
CASES = FIXTURES / "cases.csv"
STORIES = FIXTURES / "stories.csv"


async def mocked_responses(_self):
    return CASES.read_bytes(), STORIES.read_bytes()


def test_round_robin():
    assert tuple(round_robin("ABC", "D", "EF")) == ("A", "D", "E", "B", "F", "C")


def test_data_cases_property(mocker):
    mocker.patch.object(Data, "fetch_spreadsheets", new=mocked_responses)
    cases = asyncio.run(Data().cases())

    assert len(cases) == 5
    cases[0].when == date(2018, 10, 8)
    cases[-1].when == date(2018, 10, 3)
