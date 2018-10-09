import pickle
from io import BytesIO

import requests
from redis import StrictRedis
from rows import import_from_csv

from violence.models import Case, Story
from violence.settings import (
    BASE_SPREADSHEET_URL,
    CACHE_DATA_FOR,
    CASES_SPREADSHEET_GID,
    CASE_LABELS,
    REDIS_DB,
    REDIS_URL,
    STORIES_SPREADSHEET_GID,
    STORY_LABELS,
)


class Data:

    def __init__(self, refresh_cache=False):
        self.cache_key = 'cases'
        self.cache = StrictRedis.from_url(REDIS_URL, db=REDIS_DB)
        if refresh_cache:
            self.reload_from_google_spreadsheet()

    @property
    def cases(self):
        cached = self.cache.get(self.cache_key)
        if cached:
            return pickle.loads(cached)

        return self.reload_from_google_spreadsheet()

    def get(self, csv_label):
        switch = {
            'cases': CASES_SPREADSHEET_GID,
            'stories': STORIES_SPREADSHEET_GID
        }
        return requests.get(BASE_SPREADSHEET_URL + switch[csv_label]).content

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
                for tag in data.get('tags').split('|') if tag
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
        self.cache.set(self.cache_key, serialized, CACHE_DATA_FOR * 3600)
        return cases
