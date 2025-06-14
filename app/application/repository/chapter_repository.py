from abc import ABC, abstractmethod
from typing import List
from app.domain.entity.chapter_entity import ChapterEntity

class ChapterRepository(ABC):
    @abstractmethod
    def get_all() -> List[ChapterEntity]:
        pass
    
    @abstractmethod
    def get_chapter_by_id(self, chapter_id: int) -> ChapterEntity|None:
        pass