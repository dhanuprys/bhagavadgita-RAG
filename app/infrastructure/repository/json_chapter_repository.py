from app.domain.entity.chapter_entity import ChapterEntity
from app.application.repository.chapter_repository import ChapterRepository
from app.infrastructure.util.json_loader import load_json

class JsonChapterRepository(ChapterRepository):
    def __init__(self):
        self.db = []
        self.__load_data()
        
    def __load_data(self):
        data = load_json('data/3-fine-verse_number/chapters.json')
        for chapter in data:
            self.db.append(ChapterEntity(**chapter))
        
    def get_all(self):
        return self.db
    
    def get_chapter_by_id(self, chapter_id):
        for chapter in self.db:
            if chapter.id == chapter_id:
                return chapter
        return None