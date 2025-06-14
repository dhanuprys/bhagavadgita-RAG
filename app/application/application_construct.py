from app.application.service.llm_adapter import LLMCollection
from app.application.service.searcher import Searcher
from app.application.repository.chapter_repository import ChapterRepository
from app.application.repository.verse_repository import VerseRepository
from app.application.repository.verse_translation_repository import VerseTranslationRepository
from app.application.service.pattern_matching import PatternMatching
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.verse_translation_entity import VerseTranslationEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from typing import List
from abc import ABC, abstractmethod

class ApplicationConstruct(ABC):
    def __init__(
        self,
        llm_collection: LLMCollection,
        chapter_repository: ChapterRepository,
        verse_repository: VerseRepository,
        verse_translation_repository: VerseTranslationRepository,
        chapter_searcher: Searcher,
        verse_translation_searcher: Searcher,
        pattern_matching_services: List[PatternMatching]
    ):
        self.llm_collection = llm_collection
        self.chapter_repository = chapter_repository
        self.verse_repository = verse_repository
        self.verse_translation_repository = verse_translation_repository
        self.chapter_searcher = chapter_searcher
        self.verse_translation_searcher = verse_translation_searcher
        self.pattern_matching_services = pattern_matching_services
        
    def prepare_model(self):
        # Load chapter model
        print("Loading chapter model")
        if self.chapter_searcher.builded():
            self.chapter_searcher.load_index()
        else:
            self.chapter_searcher.build_index(
                self.chapter_repository.get_all()
            )
            
        # Load verse translation model
        print("Loading verse translation model")
        if self.verse_translation_searcher.builded():
            self.verse_translation_searcher.load_index()
        else:
            self.verse_translation_searcher.build_index(
                self.verse_translation_repository.get_all()
            )
            
    def get_context(self, user_input: str) -> List[ChapterEntity] | List[VerseTranslationEntity] | PatternMatchingResult | None:
        results = None
        for pattern_matching_service in self.pattern_matching_services:
            matching_result = pattern_matching_service.match(user_input)
            if matching_result:
                results = pattern_matching_service.handle(
                    self.llm_collection.general,
                    user_input,
                    matching_result
                )
                break
            
        if not results:
            if 'bab' in user_input.lower():
                print("Using chapter searcher!")
                results = self.chapter_searcher.search(user_input)
            else:
                print("Using verse searcher")
                results = self.verse_translation_searcher.search(user_input)
    
        return results
    
    @abstractmethod
    def run(self):
        pass