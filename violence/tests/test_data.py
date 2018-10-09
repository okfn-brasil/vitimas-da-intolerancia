from datetime import date
from pathlib import Path

import pytest

from violence.data import Data


FIXTURES = {
    'cases': Path() / 'violence' / 'tests' / 'fixtures' / 'cases.csv',
    'stories': Path() / 'violence' / 'tests' / 'fixtures' / 'stories.csv'
}


@pytest.fixture
def data():
    """A Data instance with cached HTTP responses from fixtures"""
    data = Data(refresh_cache=False)
    data.cache.delete(data.cache_key)

    for name, fixture in FIXTURES.items():
        with open(fixture) as fobj:
            data.cache.set(f'response-{name}', fobj.read(), 99)

    yield data

    for name in FIXTURES.keys():
        data.cache.delete(name)


def test_data_cases_property(data):
    assert len(data.cases) == 8
    data.cases[0].when == date(2018, 10, 8)
    data.cases[-1].when == date(2018, 10, 3)
