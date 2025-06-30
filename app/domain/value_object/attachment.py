from dataclasses import dataclass
from typing import Literal


@dataclass
class Attachment:
    type: Literal["audio", "url"]
    title: str
    url: str
    description: str = ""

    def to_dict(self):
        return {
            "type": self.type,
            "title": self.title,
            "url": self.url,
            "description": self.description,
        }
