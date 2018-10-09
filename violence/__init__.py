from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from violence.data import Data


app = Sanic()
jinja = SanicJinja2(app, pkg_name='violence')
app_data = Data(refresh_cache=True)
app_data.reload_from_google_spreadsheet()


@app.route("/")
@jinja.template('index.html')
async def test(request):
    return {'cases': app_data.cases}
