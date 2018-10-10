from urllib.parse import urlparse

from aiocache import cached, caches
from sanic import Sanic
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import (
    CACHE_DATA_FOR,
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


@cached(key="home")
@app.route("/")
@jinja.template("index.html")
async def home(request):
    return {"cases": app_data.cases, "title": TITLE}


@cached(key='map')
@app.route('/map')
@jinja.template('map.html')
async def map(request):
    return {'cases': app_data.cases, 'title': TITLE}
