import json
import os


def esc(s):
    """
    Escape and flatten any string so it becomes a single-line SQL literal:
    - Normalize CRLF and CR to LF
    - Replace LF with literal \n
    - Escape backslashes and single quotes
    """
    if not isinstance(s, str):
        return s
    # 1. Normalize all newlines to '\n'
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # 2. Escape backslashes first
    s = s.replace("\\", "\\\\")
    # 3. Escape single quotes
    s = s.replace("'", "\\'")
    # 4. Convert real newlines into literal \n
    s = s.replace("\n", "\\n")
    return s


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    base = "data/3-fine-verse_number/"
    out_path = "data/gita_insertion.sql"

    chapters = load_json(os.path.join(base, "chapters.json"))
    verses = load_json(os.path.join(base, "verses.json"))
    translations = load_json(os.path.join(base, "translations.json"))

    lines = ["-- MySQL Insert Script", "USE bhagavadgita;", ""]

    # Chapters
    for c in chapters:
        lines.append(
            "INSERT INTO chapters "
            "(id, chapter_number, name, name_hindi, name_sanskrit, summary, verses_count) VALUES ("
            f"{c['id']}, "
            f"{c['chapter_number']}, "
            f"'{esc(c.get('name',''))}', "
            f"'{esc(c.get('name_hindi',''))}', "
            f"'{esc(c.get('name_sanskrit',''))}', "
            f"'{esc(c.get('summary',''))}', "
            f"{c.get('verses_count',0)}"
            ");"
        )

    # Verses
    for v in verses:
        lines.append(
            "INSERT INTO verses "
            "(id, text_hindi, text_sanskrit, text_sanskrit_meanings, audio_url, chapter_id, verse_number) VALUES ("
            f"{v['id']}, "
            f"'{esc(v.get('text_hindi',''))}', "
            f"'{esc(v.get('text_sanskrit',''))}', "
            f"'{esc(v.get('text_sanskrit_meanings',''))}', "
            f"'{esc(v.get('audio_url',''))}', "
            f"{v['chapter_id']}, "
            f"{v['verse_number']}"
            ");"
        )

    # Translations
    for t in translations:
        lines.append(
            "INSERT INTO verse_translations "
            "(id, content, verse_id) VALUES ("
            f"{t['id']}, "
            f"'{esc(t.get('content',''))}', "
            f"{t['verse_id']}"
            ");"
        )

    # Write out
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✅ SQL script written to {out_path}")


if __name__ == "__main__":
    main()
