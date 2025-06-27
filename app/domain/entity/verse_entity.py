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

    def to_dict(self):
        return {
            "id": self.id,
            "verse_number": self.verse_number,
            "text_hindi": self.text_hindi,
            "text_sanskrit": self.text_sanskrit,
            "text_sanskrit_meanings": self.text_sanskrit_meanings,
            "audio_url": self.audio_url,
            "chapter_id": self.chapter_id,
        }
