import pytest

from victims import app as victims_app


@pytest.fixture
def app():
    return victims_app
