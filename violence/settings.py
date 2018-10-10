from pathlib import Path

from decouple import config

TITLE = '#VítimasDaIntolerância'

DEBUG = config('DEBUG', default='False', cast=bool)
HOST = config('HOST', default='0.0.0.0')
PORT = config('PORT', default='8000', cast=int)
STATIC_DIR = Path() / 'violence' / 'static'

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/')
REDIS_DB = config('REDIS_DB', default='0', cast=lambda x: int(x) * 3600)
CACHE_DATA_FOR = 3  # in hours
REFRESH_CACHE_ON_LOAD = config('REFRESH_CACHE_ON_LOAD', default=False, cast=bool)

SPREADSHEET_ID = config('SPREADSHEET_ID')
CASES_SPREADSHEET_GID = config('CASES_SPREADSHEET_GID')
STORIES_SPREADSHEET_GID = config('STORIES_SPREADSHEET_GID')
BASE_SPREADSHEET_URL = (
    f'https://docs.google.com/spreadsheets/u/0/d/{SPREADSHEET_ID}/'
    f'export?format=csv&id={SPREADSHEET_ID}&gid='
)

# labels from the Google Spreadsheet (converted by rows) and from our models
STORY_LABELS = (
    ('url', 'url'),
    ('veiculo', 'source'),
    ('titulo', 'title'),
    ('imagem_ou_video', 'image_or_video'),
    ('id_caso', 'case_id'),
    ('resumo', 'summary'),
)
CASE_LABELS = (
    ('id', 'id'),
    ('data', 'when'),
    ('uf', 'state'),
    ('municipio', 'city'),
    ('tags', 'tags'),
)


# tags from the Google Spreadsheet and colors from Semantic UI
TAG_COLORS = {
    'homicídio': 'red',
    'agressão': 'orange',
    'xenofobia': 'yellow',
    'prisão': 'olive',
    '': 'green',
    'ameaça': 'teal',
    '': 'blue',
    '': 'violet',
    'mulher': 'purple',
    'homofobia': 'pink',
    'jornalista': 'brown',
    '': 'grey',
    '': 'black',
}
