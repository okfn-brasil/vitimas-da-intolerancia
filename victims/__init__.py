from sanic import Sanic
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import CASE_MAX_CHARS, STATIC_DIR, TITLE


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
jinja = SanicJinja2(app, pkg_name="victims")
Compress(app)


@app.route("/")
@jinja.template("home.html")
async def home(request):
    data = Data()
    return {
        "cases": await data.cases(),
        "title": TITLE,
        "url_path": "/",
        "max_chars": CASE_MAX_CHARS,
    }


@app.route("/about.html")
@jinja.template("about.html")
async def about(request):
    return {"title": TITLE, "url_path": "/about.html"}
