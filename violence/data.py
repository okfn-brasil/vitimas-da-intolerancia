import pickle
from io import BytesIO

import redis
import requests
from decouple import config
from rows import import_from_csv


SPREADSHEET_ID = config('SPREADSHEET_ID')


class Data:

    BASE_URL = (
        f'https://docs.google.com/spreadsheets/u/0/d/{SPREADSHEET_ID}/'
        f'export?format=csv&id={SPREADSHEET_ID}&gid='
    )
    CACHE_FOR = 3  # in hours

    def __init__(self, refresh_cache=False):
        self.cache_key = 'hate-crimes-table'
        self.cache = redis.StrictRedis.from_url(
            config('REDIS_URL', default='redis://localhost:6379/'),
            db=config('REDIS_DB', default='0', cast=int)
        )
        if refresh_cache:
            self.reload_from_google_spreadsheet()

    @property
    def table(self):
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
    def _append_story(story, table):
        for case in table:
            if case['id'] != story['id_caso']:
                continue

            case['stories'] = case.get('stories') or []  # avoids getting None
            case['stories'].append(story)

    def reload_from_google_spreadsheet(self):
        with BytesIO(self.get('cases')) as buffer:
            table = sorted(
                (row._asdict() for row in import_from_csv(buffer) if row.data),
                key=lambda row: row['data'],
                reverse=True
            )

        with BytesIO(self.get('stories')) as buffer:
            for story in import_from_csv(buffer):
                self._append_story(story._asdict(), table)

        cleaned_table = tuple(row for row in table if row.get('stories'))
        serialized = pickle.dumps(cleaned_table)
        self.cache.set(self.cache_key, serialized, self.CACHE_FOR * 3600)
        return table
