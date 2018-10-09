from datetime import date
from itertools import cycle
from pathlib import Path

from violence.data import Data


FIXTURES = Path() / 'violence' / 'tests' / 'fixtures'


def test_data_get_method(mocker):
    get = mocker.patch('violence.data.requests.get')
    get.return_value.content = b'42'
    assert Data().get('cases') == b'42'
    get.assert_called_once()


def test_data_cases_property(mocker):
    get = mocker.patch.object(Data, 'get')
    with open(FIXTURES / 'cases.csv', 'rb') as cases:
        with open(FIXTURES / 'stories.csv', 'rb') as stories:
            get.side_effect = cycle((cases.read(), stories.read()))

    data = Data()
    data.reload_from_google_spreadsheet()
    assert len(data.cases) == 5
    data.cases[0].when == date(2018, 10, 8)
    data.cases[-1].when == date(2018, 10, 3)
