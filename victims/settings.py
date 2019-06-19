from pathlib import Path

from decouple import config


PROJECT_DIRECTORY = Path(__file__).parent
TITLE = "#VítimasDaIntolerância"
CASE_MAX_CHARS = config("CASE_MAX_CHARS", default=559, cast=int)  # 558 chars + …

CNAME = config("CNAME", default="www.vitimasdaintolerancia.org")

SPREADSHEET_ID = config(
    "SPREADSHEET_ID", default="1C73e7Lph1fNGontBodEDFZ4oqn3cC2oB_0Av3vRTiRw"
)
CASES_SPREADSHEET_GID = config("CASES_SPREADSHEET_GID", default="0")
STORIES_SPREADSHEET_GID = config("STORIES_SPREADSHEET_GID", default="1865357648")
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
