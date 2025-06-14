import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# === Data Entities ===

@dataclass
class VerseTranslationEntity:
    """
    Represents a translated version of a verse in a specific language.
    """
    id: int
    content: str
    verse_id: int  # Foreign key to VerseEntity
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'verse_id': self.verse_id
        }

@dataclass
class VerseEntity:
    """
    Represents a verse with its original Sanskrit, Hindi text, word meanings, and audio.
    """
    id: int
    text_hindi: str
    text_sanskrit: str
    text_sanskrit_meanings: str
    audio_url: str
    chapter_id: int  # Foreign key to ChapterEntity
    translations: List[VerseTranslationEntity] = field(default_factory=list)  # Related translations
    
    def to_dict(self):
        return {
            'id': self.id,
            'text_hindi': self.text_hindi,
            'text_sanskrit': self.text_sanskrit,
            'text_sanskrit_meanings': self.text_sanskrit_meanings,
            'audio_url': self.audio_url,
            'chapter_id': self.chapter_id,
        }

@dataclass
class ChapterEntity:
    """
    Represents a chapter consisting of a name, summary, and its verses.
    """
    id: int
    chapter_number: int
    name: str
    name_hindi: str
    name_sanskrit: str
    summary: str
    verses_count: int
    verses: List[VerseEntity] = field(default_factory=list)  # Related verses
    
    def to_dict(self):
        return {
            'id': self.id,
            'chapter_number': self.chapter_number,
            'name': self.name,
            'name_hindi': self.name_hindi,
            'name_sanskrit': self.name_sanskrit,
            'summary': self.summary,
            'verses_count': self.verses_count
        }


# === Repository Interfaces ===

class Repository(ABC):
    """
    Abstract base repository interface.
    """

    @abstractmethod
    def get_all(self):
        """
        Retrieve all entities.
        """
        pass

    @abstractmethod
    def get_by_id(self, id):
        """
        Retrieve an entity by its ID.
        """
        pass


class VerseTranslationRepository(Repository):
    """
    Interface for verse translation repositories.
    """

    def get_by_verse_id(self, id) -> List[VerseTranslationEntity]:
        """
        Retrieve all translations for a specific verse.
        """
        pass

class VerseRepository(Repository):
    """
    Interface for verse repositories.
    """

    def get_by_chapter_id(self, id) -> List[VerseEntity]:
        """
        Retrieve all verses for a specific chapter.
        """
        pass
    
class ChapterRepository(Repository):
    """
    Interface for chapter repositories.
    """
    pass


# === Utility Loader ===

class JsonLoader:
    """
    Loads and holds JSON data from file into memory.
    """

    def __init__(self):
        self.db = []

    def load(self, filename):
        """
        Load JSON data from the given file.
        """
        with open(filename) as json_file:
            self.db = json.load(json_file)


# === Concrete Repositories ===

class JsonVerseTranslationRepository(JsonLoader, VerseRepository):
    """
    Loads verse translations from JSON and filters only English entries.
    """

    def __init__(self, filename):
        super().__init__()
        self.load(filename)
        self.__normalize()

    def __normalize(self):
        new_data = []
        index = 1
        for data in self.db:
            if data['lang'] != 'english':
                continue

            new_data.append(VerseTranslationEntity(
                id=index,
                content=data['description'],
                verse_id=data['verse_id']
            ))
            index += 1
            
        self.db = new_data

    def get_all(self):
        return self.db

    def get_by_id(self, id):
        for verse in self.db:
            if verse.id == id:
                return verse

    def get_by_verse_id(self, id) -> List[VerseTranslationEntity]:
        """
        Get all English translations by verse ID.
        """
        verses = []
        for verse in self.db:
            if verse.verse_id == id:
                verses.append(verse)
        return verses


class JsonVerseRepository(JsonLoader, VerseRepository):
    """
    Loads verses from JSON and maps them to VerseEntity with translations and audio URLs.
    """

    def __init__(self, filename, verse_translation_repository: VerseTranslationRepository):
        super().__init__()
        self.load(filename)
        self.__verse_translation_repository = verse_translation_repository
        self.__normalize()

    def __normalize(self):
        """
        Normalize raw JSON data into structured VerseEntity list.
        Includes mapping translations and audio URL generation.
        """
        for i in range(len(self.db)):
            current = self.db[i]
            translations = self.__get_translation_by_verse_id(current['id'])

            self.db[i] = VerseEntity(
                id=current['id'],
                text_hindi=current['text'],
                text_sanskrit=current['transliteration'],
                text_sanskrit_meanings=current['word_meanings'],
                audio_url='https://gita.github.io/gita/data/verse_recitation/%d/%d.mp3' % (
                    current['chapter_id'], current['id']),
                chapter_id=current['chapter_id'],
                translations=translations
            )

    def get_all(self):
        return self.db

    def get_by_id(self, id):
        for verse in self.db:
            if verse.id == id:
                return verse

    def get_by_chapter_id(self, id) -> List[VerseEntity]:
        """
        Return all verses that belong to a given chapter.
        """
        verses = []
        for verse in self.db:
            if verse.chapter_id == id:
                verses.append(verse)
        return verses

    def __get_translation_by_verse_id(self, id) -> List[VerseTranslationEntity]:
        """
        Internal method to retrieve translations using repository.
        """
        return self.__verse_translation_repository.get_by_verse_id(id)


class JsonChapterRepository(JsonLoader, ChapterRepository):
    """
    Loads chapters from JSON and includes their related verses using VerseRepository.
    """

    def __init__(self, filename, verse_repository: VerseRepository):
        super().__init__()
        self.load(filename)
        self.__verse_repository = verse_repository
        self.__normalize()

    def __normalize(self):
        """
        Normalize raw JSON data into structured ChapterEntity list, with nested verses.
        """
        for i in range(len(self.db)):
            current = self.db[i]
            self.db[i] = ChapterEntity(
                id=current['id'],
                chapter_number=current['chapter_number'],
                name=current['name_meaning'],
                name_sanskrit=current['name_transliterated'],
                name_hindi=current['name'],
                summary=current['chapter_summary'],
                verses_count=current['verses_count'],
                verses=self.__get_verse_by_chapter_id(current['id'])
            )

    def get_all(self) -> List[ChapterEntity]:
        return self.db

    def get_by_id(self, id) -> ChapterEntity:
        for chapter in self.db:
            if chapter.id == id:
                return chapter

    def __get_verse_by_chapter_id(self, id) -> List[VerseEntity]:
        """
        Internal method to retrieve verses belonging to a chapter.
        """
        return self.__verse_repository.get_by_chapter_id(id)


# === Example Usage ===

def json_dumps_hindi(data_list):
    return json.dumps(
        data_list,
        ensure_ascii=False,
        indent=4
    )

# Initialize repositories with JSON files
verse_translation_repository = JsonVerseTranslationRepository('data/raw/translation.json')
verse_repository = JsonVerseRepository('data/raw/verse.json', verse_translation_repository)
chapter_repository = JsonChapterRepository('data/raw/chapters.json', verse_repository)

with open('data/1-fine-restructured/chapters.json', 'w') as file:
    file.write(
        json_dumps_hindi([chapter.to_dict() for chapter in chapter_repository.get_all()])
    )
    
with open('data/1-fine-restructured/verses.json', 'w') as file:
    file.write(
        json_dumps_hindi([verse.to_dict() for verse in verse_repository.get_all()])
    )
    
with open('data/1-fine-restructured/translations.json', 'w') as file:
    file.write(
        json_dumps_hindi([translation.to_dict() for translation in verse_translation_repository.get_all()])
    )