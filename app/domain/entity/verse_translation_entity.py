from dataclasses import dataclass


@dataclass
class VerseTranslationEntity:
    id: int
    content: str
    verse_id: int
