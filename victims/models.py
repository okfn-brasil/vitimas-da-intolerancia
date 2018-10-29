import json

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
        skip_sources = {"twitter", "facebook"}
        if self.source.lower() in skip_sources:
            return False

        if not self.title:
            return False

        if not self.image_or_video:
            return False

        return True

    def to_json(self):
        items = {
            "url": self.url,
            "source": self.source,
            "title": self.title,
            "image_or_video": self.image_or_video,
            "summary": self.summary,
            "case_id": self.case_id,
        }
        return json.dumps(items, sort_keys=True)


@dataclass
class Case:
    id: int
    aggressor_side: str
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
        return ((tag, TAG_COLORS.get(tag, "grey")) for tag in self.tags)

    def is_valid(self):
        return bool(self.when)

    def to_json(self):
        items = {
            "id": self.id,
            "aggressor_side": self.aggressor_side,
            "when": str(self.when),
            "state": self.state,
            "city": self.city,
            "tags": self.tags,
            "stories": [story.to_JSON() for story in self.stories],
        }
        return json.dumps(items, sort_keys=True)
