import asyncio
from io import BytesIO
from itertools import groupby, zip_longest
from random import shuffle

import aiohttp
from rows import import_from_csv

from victims.models import Case, Story
from victims.settings import (
    BASE_SPREADSHEET_URL,
    CASES_SPREADSHEET_GID,
    CASE_LABELS,
    STORIES_SPREADSHEET_GID,
    STORY_LABELS,
)


def round_robin(*iterables):
    """('ABC', 'D', 'EF') --> ('A', 'D', 'E', 'B', 'F', 'C')"""
    for sequence in zip_longest(*iterables):
        yield from (item for item in sequence if item)


class Data:
    async def fetch(self, session, url):
        async with session.get(url) as response:
            print(f"Fetching {url}")
            print(f"Fetching {url}")
            print(f"Fetching {url}")
            return await response.read()

    async def fetch_spreadsheets(self):
        loop = asyncio.get_event_loop()
        urls = (
            BASE_SPREADSHEET_URL + CASES_SPREADSHEET_GID,
            BASE_SPREADSHEET_URL + STORIES_SPREADSHEET_GID,
        )
        async with aiohttp.ClientSession(loop=loop) as session:
            requests = tuple(self.fetch(session, url) for url in urls)
            return await asyncio.gather(*requests)

    def serialize_cases(self, buffer):
        for case in import_from_csv(buffer):
            case = case._asdict()
            data = {new: case.get(old) for old, new in CASE_LABELS}

            data["stories"] = data.get("stories") or []  # avoids getting None
            data["tags"] = data.get("tags") or ""  # avoids getting None
            data["tags"] = data["tags"].split("|")
            data["tags"] = [tag.strip().lower() for tag in data["tags"] if tag]

            case = Case(**data)
            if not case.is_valid():
                continue

            yield case

    def append_stories(self, buffer, cases):
        for story in import_from_csv(buffer):
            story = story._asdict()
            data = {
                new_label: story.get(old_label) for old_label, new_label in STORY_LABELS
            }
            story = Story(**data)
            if not story.is_valid():
                continue

            for case in cases:  # append all stories
                if case.id != story.case_id:
                    continue

                case.stories.append(story)
                break

            for case in cases:  # shuffle stories order
                if case.id != story.case_id:
                    continue

                shuffle(case.stories)
                break

        return cases

    async def cases(self):
        cases, stories = await self.fetch_spreadsheets()
        aggressor_getter = lambda case: case.aggressor_side
        when_getter = lambda case: case.when

        with BytesIO(cases) as buffer:
            # Ordering cases: first by when, then round robin aggressor_side
            cases = sorted(self.serialize_cases(buffer), key=aggressor_getter)
            groups = groupby(cases, key=aggressor_getter)
            iterators = (
                sorted(group, key=when_getter, reverse=True) for _, group in groups
            )
            cases = tuple(round_robin(*iterators))

        with BytesIO(stories) as buffer:
            cases = self.append_stories(buffer, cases)

        return tuple(case for case in cases if case.stories)
