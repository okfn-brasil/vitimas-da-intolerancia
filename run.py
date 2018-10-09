from decouple import config

from violence import app


app.run(
    host=config('HOST', default='0.0.0.0'),
    port=config('PORT', default='8000', cast=int),
    debug=config('DEBUG', default='False', cast=bool)
)
