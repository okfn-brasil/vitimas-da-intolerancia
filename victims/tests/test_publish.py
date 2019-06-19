from collections import namedtuple

import pytest

from victims import publish
from victims.settings import CNAME


@pytest.fixture
def options():
    keys = ("use_shell", "branch", "mesg", "followlinks", "nojekyll", "cname")
    values = (False, "gh-pages", "Publish website", False, False, CNAME)
    Options = namedtuple("Options", keys)
    return Options(*values)


def test_subrocess_is_called(app, options, mocker):
    Git = mocker.patch("victims.Git")
    run_import = mocker.patch("victims.run_import")

    runner = app.test_cli_runner()
    runner.invoke(publish)

    Git.assert_called_once_with()
    Git.return_value.check_call.assert_called_once_with("push", "origin", "gh-pages")
    run_import.assert_called_once_with(Git.return_value, "build", options)


def test_subrocess_is_called_with_force_argument(app, options, mocker):
    Git = mocker.patch("victims.Git")
    run_import = mocker.patch("victims.run_import")

    runner = app.test_cli_runner()
    runner.invoke(publish, ["--force"])

    Git.assert_called_once_with()
    Git.return_value.check_call.assert_called_once_with(
        "push", "origin", "gh-pages", "--force"
    )
    run_import.assert_called_once_with(Git.return_value, "build", options)
