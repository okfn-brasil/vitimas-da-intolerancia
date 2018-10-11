import asyncio
import pickle
from io import BytesIO
from itertools import cycle, groupby, islice
from random import shuffle

import aiohttp
from redis import StrictRedis
from rows import import_from_csv

from victims.models import Case, Story
from victims.settings import (
    BASE_SPREADSHEET_URL,
    CACHE_DATA_FOR,
    CASES_SPREADSHEET_GID,
    CASE_LABELS,
    REDIS_DB,
    REDIS_URL,
    STORIES_SPREADSHEET_GID,
    STORY_LABELS,
)


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


class Data:
    def __init__(self, refresh_cache=False):
        self.cache_key = "cases"
        self.cache = StrictRedis.from_url(REDIS_URL, db=REDIS_DB)
        self.urls = {
            "cases": BASE_SPREADSHEET_URL + CASES_SPREADSHEET_GID,
            "stories": BASE_SPREADSHEET_URL + STORIES_SPREADSHEET_GID,
        }

        if refresh_cache:
            self.reload_from_google_spreadsheet()

    async def fetch(self, session, name):
        async with session.get(self.urls[name]) as response:
            contents = await response.read()
            self.cache.set(f"response-{name}", contents, CACHE_DATA_FOR)

    async def _get_spreadsheets(self, loop):
        names = self.urls.keys()
        async with aiohttp.ClientSession(loop=loop) as session:
            requests = tuple(self.fetch(session, name) for name in names)
            await asyncio.gather(*requests)

    def get_spreadsheets(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._get_spreadsheets(loop))

    def get_spreadsheet(self, name):
        key = f"response-{name}"
        cached = self.cache.get(key)
        if cached:
            return cached

        self.get_spreadsheets()  # cache responses
        return self.get_spreadsheet(name)

    @property
    def cases(self):
        cached = self.cache.get(self.cache_key)
        if cached:
            return self.shuffle_cases(pickle.loads(cached))

        return self.shuffle_cases(self.reload_from_google_spreadsheet())

    def serialize_cases(self, buffer):
        for case in import_from_csv(buffer):
            case = case._asdict()
            data = {
                new_label: case.get(old_label) for old_label, new_label in CASE_LABELS
            }

            data["stories"] = data.get("stories") or []  # avoids getting None
            data["tags"] = data.get("tags") or ""  # avoids getting None
            data["tags"] = [
                tag.strip().lower() for tag in data.get("tags").split("|") if tag
            ]

            case = Case(**data)
            if not case.is_valid():
                continue

            yield case

    def shuffle_cases(self, cases):
        for case in cases:
            shuffle(case.stories)

        return cases

    def append_stories(self, buffer, cases):
        for story in import_from_csv(buffer):
            story = story._asdict()
            data = {
                new_label: story.get(old_label) for old_label, new_label in STORY_LABELS
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
        aggressor_getter = lambda case: case.aggressor_side
        when_getter = lambda case: case.when

        with BytesIO(self.get_spreadsheet("cases")) as buffer:
            # Ordering cases: first by when, then round robin aggressor_side
            cases = sorted(
                self.serialize_cases(buffer), key=aggressor_getter,
            )
            groups = groupby(cases, key=aggressor_getter)
            iterators = [
                sorted(group, key=when_getter, reverse=True) for _, group in groups
            ]
            cases = list(roundrobin(*iterators))

        with BytesIO(self.get_spreadsheet("stories")) as buffer:
            cases = self.append_stories(buffer, cases)

        cleaned_cases = tuple(case for case in cases if case.stories)
        serialized = pickle.dumps(cleaned_cases)
        self.cache.set(self.cache_key, serialized, CACHE_DATA_FOR * 3600)
        return cases
