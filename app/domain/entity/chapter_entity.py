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