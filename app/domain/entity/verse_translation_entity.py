from dataclasses import dataclass


@dataclass
class VerseTranslationEntity:
    id: int
    content: str
    verse_id: int

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "verse_id": self.verse_id,
        }
