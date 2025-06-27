from dataclasses import dataclass


@dataclass
class ChapterEntity:
    id: int
    chapter_number: int
    name: str
    name_hindi: str
    name_sanskrit: str
    summary: str
    verses_count: int

    def to_dict(self):
        return {
            "id": self.id,
            "chapter_number": self.chapter_number,
            "name": self.name,
            "name_hindi": self.name_hindi,
            "name_sanskrit": self.name_sanskrit,
            "summary": self.summary,
            "verses_count": self.verses_count,
        }
