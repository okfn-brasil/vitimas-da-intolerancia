from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from hate_crimes_monitor.data import Data


app = Sanic()
jinja = SanicJinja2(app, pkg_name='hate_crimes_monitor')
app_data = Data(refresh_cache=True)


@app.route("/")
@jinja.template('index.html')
async def test(request):
    return {'table': app_data.table}
