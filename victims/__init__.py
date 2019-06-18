from urllib.parse import urlunparse

from sanic import Sanic
from sanic.response import redirect
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import CASE_MAX_CHARS, DEBUG, STATIC_DIR, TITLE


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
jinja = SanicJinja2(app, pkg_name="victims")
Compress(app)


@app.middleware("request")
def force_https(request):
    if DEBUG:
        return None

    host = request.headers.get("Host", "")
    protocol = "https" if request.transport.get_extra_info("sslcontext") else "http"

    if request.headers.get("x-forwarded-proto", protocol) == "http":
        args = ("https", host, request.path, None, request.query_string, None)
        url = urlunparse(args)
        return redirect(url)


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
