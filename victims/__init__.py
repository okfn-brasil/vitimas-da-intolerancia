import pickle
from urllib.parse import urlunparse

from aioredis import create_redis
from sanic import Sanic
from sanic.response import json, redirect
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from victims.data import Data
from victims.settings import CASE_MAX_CHARS, DEBUG, REDIS_URL, STATIC_DIR, TITLE


app = Sanic("vitimas_da_intolerancia")
app.static("/static", str(STATIC_DIR))
jinja = SanicJinja2(app, pkg_name="victims")
Compress(app)


async def clear_cache():
    redis = await create_redis(REDIS_URL)
    keys = len(await redis.keys("*"))
    print(f"Flushing {keys} key/value pair(s)")
    await redis.flushall()
    redis.close()
    await redis.wait_closed()
    print("Done :)")


@app.listener("before_server_start")
async def before_start(app, loop):
    await clear_cache()


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
    redis = await create_redis(REDIS_URL)
    cases = await redis.get("cases")

    if cases:
        cases = pickle.loads(cases)
    else:
        data = Data()
        cases = await data.cases()
        await redis.set("cases", pickle.dumps(cases))

    redis.close()
    await redis.wait_closed()

    return {
        "cases": cases,
        "title": TITLE,
        "url_path": "/",
        "max_chars": CASE_MAX_CHARS,
    }


@app.route("/about.html")
@jinja.template("about.html")
async def about(request):
    return {"title": TITLE, "url_path": "/about.html"}


@app.route("/data.json")
async def data(request):
    cases = await get_cases()
    cases = [case.to_JSON() for case in cases]
    return json(cases)
