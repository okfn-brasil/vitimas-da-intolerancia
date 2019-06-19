from subprocess import PIPE

from flask_frozen import Freezer

from victims import publish
from victims.settings import CNAME


def test_subrocess_is_called(app, mocker):
    Popen = mocker.patch("victims.Popen")
    runner = app.test_cli_runner()
    runner.invoke(publish)
    Popen.assert_called_once_with(
        ["ghp-import", "--cname", CNAME, "--push", "--force", "build/"],
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE,
    )
