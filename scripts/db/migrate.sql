-- CREATE DATABASE bhagavadgita;
-- USE bhagavadgita;

-- Chapters Table
CREATE TABLE chapters (
    id INT PRIMARY KEY,
    chapter_number INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_hindi VARCHAR(255) NOT NULL,
    name_sanskrit VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    verses_count INT NOT NULL
);

-- Index for faster lookup on chapter_number
CREATE INDEX idx_chapters_chapter_number ON chapters(chapter_number);

-- Verses Table
CREATE TABLE verses (
    id INT PRIMARY KEY,
    text_hindi TEXT NOT NULL,
    text_sanskrit TEXT NOT NULL,
    text_sanskrit_meanings TEXT NOT NULL,
    audio_url VARCHAR(512) NOT NULL,
    chapter_id INT NOT NULL,
    verse_number INT NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id)
);

-- Indexes for performance
CREATE INDEX idx_verses_chapter_id ON verses(chapter_id);
CREATE INDEX idx_verses_verse_number ON verses(verse_number);
CREATE INDEX idx_verses_chapter_verse ON verses(chapter_id, verse_number); -- for composite lookup

-- Verse Translations Table
CREATE TABLE verse_translations (
    id INT PRIMARY KEY,
    content TEXT NOT NULL,
    verse_id INT NOT NULL,
    FOREIGN KEY (verse_id) REFERENCES verses(id)
);

-- Index for faster lookup on verse_id
CREATE INDEX idx_verse_translations_verse_id ON verse_translations(verse_id);
