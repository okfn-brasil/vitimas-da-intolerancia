from flask_frozen import Freezer

from victims import build


def test_freeze_is_called(app, mocker):
    freeze = mocker.patch.object(Freezer, "freeze")
    runner = app.test_cli_runner()
    runner.invoke(build)
    freeze.assert_called_once_with()
