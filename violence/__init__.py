from sanic import Sanic
from sanic_compress import Compress
from sanic_jinja2 import SanicJinja2

from violence.data import Data
from violence.settings import (
    REFRESH_CACHE_ON_LOAD,
    STATIC_DIR,
    TITLE
)


app = Sanic('violencia_nao_tem_partido')
app.static('/static', str(STATIC_DIR))
Compress(app)
jinja = SanicJinja2(app, pkg_name='violence')
app_data = Data(refresh_cache=REFRESH_CACHE_ON_LOAD)


@app.route('/')
@jinja.template('index.html')
async def index(request):
    return {'cases': app_data.cases}
    return {'cases': app_data.cases, 'title': TITLE}
