from dataclasses import dataclass

@dataclass
class VerseEntity:
    id: int
    verse_number: int
    text_hindi: str
    text_sanskrit: str
    text_sanskrit_meanings: str
    audio_url: str
    chapter_id: int
