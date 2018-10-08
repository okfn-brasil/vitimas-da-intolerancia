from datetime import date
from pathlib import Path

from violence.data import Data


FIXTURES = Path() / 'violence' / 'tests' / 'fixtures'


def test_data_get_method(mocker):
    get = mocker.patch('violence.data.requests.get')
    get.return_value.content = b'42'
    assert Data().get('cases') == b'42'
    get.assert_called_once()


def test_data_table_property(mocker):
    get = mocker.patch.object(Data, 'get')
    with open(FIXTURES / 'cases.csv', 'rb') as cases:
        with open(FIXTURES / 'stories.csv', 'rb') as stories:
            get.side_effect = (cases.read(), stories.read())

    table = Data().table
    assert len(table) == 8
    table[0]['data'] == date(2018, 10, 8)
    table[-1]['data'] == date(2018, 10, 3)
