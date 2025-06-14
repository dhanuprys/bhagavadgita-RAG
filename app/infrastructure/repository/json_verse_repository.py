from app.domain.entity.verse_entity import VerseEntity
from app.application.repository.verse_repository import VerseRepository
from app.infrastructure.util.json_loader import load_json

class JsonVerseRepository(VerseRepository):
    def __init__(self):
        self.db = []
        self.__load_data()
        
    def __load_data(self):
        data = load_json('data/3-fine-verse_number/verses.json')
        for verse in data:
            self.db.append(VerseEntity(**verse))
        
    def get_all(self):
        return self.db
    
    def get_by_verse_id(self, verse_id):
        for verse in self.db:
            if verse.id == verse_id:
                return verse
        return None