from datetime import date
from unittest.mock import PropertyMock

from violence import app
from violence.data import Data


TABLE = (
    {
        'data': date(2018, 10, 7),
        'stories': (
            {
                'url': 'https://foo.bar/',
                'titulo': 'Foo Bar',
                'imagem_ou_video': 'https://imgs.foo.bar/avatar.png'
            },
        )
    },
)


def test_home_status(mocker):
    table = mocker.patch.object(Data, 'table', new_callable=PropertyMock)
    table.return_value = TABLE
    _, response = app.test_client.get('/')
    assert response.status == 200


def test_home_contents(mocker):
    table = mocker.patch.object(Data, 'table', new_callable=PropertyMock)
    table.return_value = TABLE
    _, response = app.test_client.get('/')
    expected_terms = (
        '07/10/2018',
        'Foo Bar',
        'https://foo.bar/',
        'https://imgs.foo.bar/avatar.png',
    )
    for expected in expected_terms:
        assert expected in response.text
