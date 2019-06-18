import asyncio

from flask import Flask, render_template
from flask_frozen import Freezer

from victims.data import Data
from victims.settings import CASE_MAX_CHARS, PROJECT_DIRECTORY, TITLE


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
