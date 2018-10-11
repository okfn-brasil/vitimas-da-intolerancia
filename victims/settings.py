from pathlib import Path
from urllib.parse import urlparse

from decouple import config


TITLE = "#VítimasDaIntolerância"

DEBUG = config("DEBUG", default="False", cast=bool)
HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", default="8000", cast=int)
STATIC_DIR = Path() / "victims" / "static"

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379/")
REDIS_DB = config("REDIS_DB", default="0", cast=int)
CACHE = {
    "default": {
        "cache": "aiocache.RedisCache",
        "timeout": config("CACHE_DATA_FOR", default="3", cast=int) * 3600,
        "endpoint": urlparse(REDIS_URL).hostname,
        "port": urlparse(REDIS_URL).port,
        "db": REDIS_DB,
        "serializer": {"class": "aiocache.serializers.StringSerializer"},
    }
}

SPREADSHEET_ID = config("SPREADSHEET_ID")
CASES_SPREADSHEET_GID = config("CASES_SPREADSHEET_GID")
STORIES_SPREADSHEET_GID = config("STORIES_SPREADSHEET_GID")
BASE_SPREADSHEET_URL = (
    f"https://docs.google.com/spreadsheets/u/0/d/{SPREADSHEET_ID}/"
    f"export?format=csv&id={SPREADSHEET_ID}&gid="
)

# labels from the Google Spreadsheet (converted by rows) and from our models
STORY_LABELS = (
    ("url", "url"),
    ("veiculo", "source"),
    ("titulo", "title"),
    ("imagem_ou_video", "image_or_video"),
    ("id_caso", "case_id"),
    ("resumo", "summary"),
)
CASE_LABELS = (
    ("id", "id"),
    ("data", "when"),
    ("uf", "state"),
    ("municipio", "city"),
    ("tags", "tags"),
    ("lado_agressor", "aggressor_side"),
)


# tags from the Google Spreadsheet and colors from Semantic UI
TAG_COLORS = {
    "homicídio": "red",
    "agressão": "orange",
    "xenofobia": "yellow",
    "prisão": "olive",
    "crime ambiental": "green",
    "ameaça": "teal",
    "crime eleitoral": "blue",
    "assédio moral": "violet",
    "mulher": "purple",
    "homofobia": "pink",
    "jornalista": "brown",
    "": "grey",  # used as default color
    "vandalismo": "black",
}
