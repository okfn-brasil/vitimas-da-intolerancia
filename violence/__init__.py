from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from violence.data import Data
from violence.settings import REFRESH_CACHE_ON_LOAD


app = Sanic()
jinja = SanicJinja2(app, pkg_name='violence')
app_data = Data(refresh_cache=REFRESH_CACHE_ON_LOAD)


@app.route("/")
@jinja.template('index.html')
async def test(request):
    return {'cases': app_data.cases}
