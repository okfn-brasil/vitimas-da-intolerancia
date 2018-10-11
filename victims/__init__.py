from urllib.parse import urlparse, urlunparse

from aiocache import cached, caches
from sanic import Sanic
from sanic.response import redirect
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import (
    CACHE_DATA_FOR,
    DEBUG,
    REDIS_DB,
    REDIS_URL,
    REFRESH_CACHE_ON_LOAD,
    STATIC_DIR,
    TITLE,
)


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
Compress(app)

jinja = SanicJinja2(app, pkg_name="victims")
app_data = Data(refresh_cache=REFRESH_CACHE_ON_LOAD)
redis = urlparse(REDIS_URL)
caches.set_config(
    {
        "default": {
            "cache": "aiocache.RedisCache",
            "namespace": "sanic-cache",
            "timeout": CACHE_DATA_FOR,
            "endpoint": redis.hostname,
            "port": redis.port,
            "db": REDIS_DB,
            "serializer": {"class": "aiocache.serializers.PickleSerializer"},
        }
    }
)


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


@cached(key="home")
@app.route("/")
@jinja.template("home.html")
async def home(request):
    return {"cases": app_data.cases, "title": TITLE, "url_path": "/"}


@cached(key="about")
@app.route("/about.html")
@jinja.template("about.html")
async def about(request):
    return {"title": TITLE, "url_path": "/about.html"}


@cached(key='map')
@app.route('/map.html')
@jinja.template('map.html')
async def map(request):
    return {"cases": app_data.cases, "title": TITLE, "url_path": "/map.html"}
