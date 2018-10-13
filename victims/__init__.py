from urllib.parse import urlunparse

from aiocache import cached, caches
from sanic import Sanic
from sanic.response import json, redirect
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import CACHE, DEBUG, STATIC_DIR, TITLE


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
jinja = SanicJinja2(app, pkg_name="victims")
caches.set_config(CACHE)
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


@cached(key="cases")
async def get_cases():
    data = Data()
    return await data.cases()


@app.route("/")
@jinja.template("home.html")
async def home(request):
    return {"cases": await get_cases(), "title": TITLE, "url_path": "/"}


@app.route("/about.html")
@jinja.template("about.html")
async def about(request):
    return {"title": TITLE, "url_path": "/about.html"}


@app.route("/data.json")
async def data(request):
    cases = await get_cases()
    cases = [case.to_JSON() for case in cases]
    return json(cases)
