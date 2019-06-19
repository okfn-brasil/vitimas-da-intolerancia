import asyncio
from collections import namedtuple

import click
from flask import Flask, render_template
from flask_frozen import Freezer
from ghp_import import Git, run_import

from victims.data import Data
from victims.settings import CASE_MAX_CHARS, CNAME, PROJECT_DIRECTORY, TITLE


app = Flask(
    "vitimas-da-intolerância",
    static_folder=PROJECT_DIRECTORY / "static",
    template_folder=PROJECT_DIRECTORY / "templates",
)


def render(template, **kwargs):
    url_path = f"/{template}" if template != "home.html" else "/"
    context = {"title": TITLE, "url_path": url_path}
    if kwargs:
        context.update(kwargs)
    return render_template(template, **context)


@app.route("/")
def home():
    data = Data()
    cases = asyncio.run(data.cases())
    return render("home.html", cases=cases, max_chars=CASE_MAX_CHARS)


@app.route("/about.html")
def about():
    return render("about.html")


@app.cli.command()
def build():
    """Build the static files version of this website."""
    freezer = Freezer(app)
    freezer.freeze()


@app.cli.command()
@click.option("--force", is_flag=True)
def publish(force):
    """Publish build/ contents to gh-pages branch using `ghp-import`."""
    git = Git()
    args = ["push", "origin", "gh-pages"]
    if force:
        args.append("--force")

    # lets mock the optparse object
    keys = ("use_shell", "branch", "mesg", "followlinks", "nojekyll", "cname")
    values = (False, "gh-pages", "Publish website", False, False, CNAME)
    Options = namedtuple("Options", keys)
    options = Options(*values)

    # run ghp-import
    run_import(git, "build", options)
    git.check_call(*args)
