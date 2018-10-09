import pickle
from io import BytesIO

import redis
import requests
from decouple import config
from rows import import_from_csv

from violence.models import Case, Story


SPREADSHEET_ID = config('SPREADSHEET_ID')
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


class Data:

    BASE_URL = (
        f'https://docs.google.com/spreadsheets/u/0/d/{SPREADSHEET_ID}/'
        f'export?format=csv&id={SPREADSHEET_ID}&gid='
    )
    CACHE_FOR = 3  # in hours

    def __init__(self, refresh_cache=False):
        self.cache_key = 'cases'
        self.cache = redis.StrictRedis.from_url(
            config('REDIS_URL', default='redis://localhost:6379/'),
            db=config('REDIS_DB', default='0', cast=int)
        )
        if refresh_cache:
            self.reload_from_google_spreadsheet()

    @property
    def cases(self):
        cached = self.cache.get(self.cache_key)
        if cached:
            return pickle.loads(cached)

        return self.reload_from_google_spreadsheet()

    def get(self, csv_label):
        mapping = {'cases': '1261886381', 'stories': '0'}
        gid = mapping.get(csv_label)
        if not gid:
            return

        return requests.get(self.BASE_URL + gid).content

    @staticmethod
    def serialize_cases(buffer):
        for case in import_from_csv(buffer):
            case = case._asdict()
            data = {
                new_label: case.get(old_label)
                for old_label, new_label in CASE_LABELS
            }

            data['stories'] = data.get('stories') or []  # avoids getting None
            data['tags'] = data.get('tags') or ''  # avoids getting None
            data['tags'] = [
                tag.strip().lower()
                for tag in data.get('tags').split('|')
            ]

            case = Case(**data)
            if case.when:
                yield case

    @staticmethod
    def append_stories(buffer, cases):
        for story in import_from_csv(buffer):
            story = story._asdict()
            data = {
                new_label: story.get(old_label)
                for old_label, new_label in STORY_LABELS
            }
            story = Story(**data)
            if not story.is_valid():
                continue

            for case in cases:
                if case.id != story.case_id:
                    continue

                case.stories.append(story)
                break

        return cases

    def reload_from_google_spreadsheet(self):
        with BytesIO(self.get('cases')) as buffer:
            cases = sorted(
                self.serialize_cases(buffer),
                key=lambda case: case.when,
                reverse=True
            )

        with BytesIO(self.get('stories')) as buffer:
            cases = self.append_stories(buffer, cases)

        cleaned_cases = tuple(case for case in cases if case.stories)
        serialized = pickle.dumps(cleaned_cases)
        self.cache.set(self.cache_key, serialized, self.CACHE_FOR * 3600)
        return cases
