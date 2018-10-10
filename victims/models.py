from dataclasses import dataclass
from datetime import date
from typing import List

from victims.settings import TAG_COLORS


@dataclass
class Story:
    url: str
    source: str
    title: str
    image_or_video: str
    summary: str
    case_id: int

    def is_valid(self):
        skip_sources = {'twitter', 'facebook'}
        if self.source.lower() in skip_sources:
            return False

        if not self.title:
            return False

        if not self.image_or_video:
            return False

        return True


@dataclass
class Case:
    id: int
    when: date
    state: str
    city: str
    tags: List[str]
    stories: List[Story]

    @property
    def main_story(self):
        return self.stories[0] if self.stories else None

    @property
    def tags_and_colors(self):
        return (
            (tag, TAG_COLORS.get(tag))
            for tag in self.tags
        )

    def is_valid(self):
        return bool(self.when)
