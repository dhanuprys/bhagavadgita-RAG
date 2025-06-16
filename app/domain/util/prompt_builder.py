from typing import List

from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity


def build_for_gita(verse_translations: List[GitaEntity], question: str):
    context = "\n".join(
        [
            f"Bab {v.c_chapter_number} - Nama Bab {v.c_name} - Sloka {v.v_verse_number} mengatakan {v.vt_content}\n"
            for v in verse_translations
        ]
    )

    return f"""
Kamu adalah asisten spiritual yang membantu menjelaskan isi Bhagavad Gita.

Aturan menjawab:
Jawablah pertanyaan HANYA berdasarkan konteks yang diberikan. 
JIKA KONTEKS TIDAK MEMUAT INFORMASI YANG RELEVAN, jawab: "Saya tidak menemukan jawaban dalam konteks yang diberikan."
At least use one paragraph of answer and maximum is 2 paragraph.
Gunakan kalimat dan kata yang jelas serta tidak redundan atau berulang.
SELALU SEMATKAN BEBERAPA INFORMASI DARI KONTEKS SECARA LANGSUNG PADA JAWABAN.

[CONTEXT]
{context}
[/CONTEXT]

Pertanyaan:
{question}

Jawaban:
"""


def build_for_chapters(chapters: List[ChapterEntity], question: str):
    context = "\n".join(
        [
            f'BAB {v.chapter_number} - Nama BAB {v.name} - Ringkasan {v.summary}"'
            for v in chapters
        ]
    )

    return f"""
Kamu adalah asisten spiritual yang membantu menjelaskan isi Bhagavad Gita.

Jawablah pertanyaan HANYA berdasarkan konteks yang diberikan. 
Jika konteks tidak memuat informasi yang relevan, jawab:
"Saya tidak menemukan jawaban dalam konteks yang diberikan.".
Selalu berikan jawaban yang singkat dan padat dalam satu paragraf saja dan gunakan bahasa yang formal.

Konteks:
{context}

Pertanyaan:
{question}

Jawaban:
"""
