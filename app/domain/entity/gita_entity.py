from dataclasses import dataclass


@dataclass
class GitaEntity:
    vt_id: int
    vt_content: str
    v_id: int
    v_text_sanskrit_meanings: str
    v_verse_number: int
    c_id: int
    c_chapter_number: int
    c_name: str
    c_summary: str
    c_verses_count: int
