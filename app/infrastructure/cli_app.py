from app.application.application_construct import ApplicationConstruct
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.verse_translation_entity import VerseTranslationEntity
import app.domain.util.prompt_builder as prompt_builder

class CLIApp(ApplicationConstruct):
    def run(self):
        self.prepare_model()
        self.run_loop()
        
    def run_loop(self):
        while True:
            user_input = self.retrieve_user_input()
            results = self.get_context(user_input)
                    
            if not results:
                print("No results found")
                continue
            
            if isinstance(results, PatternMatchingResult):
                print(results.output)
            else:
                prompt = None
                if isinstance(results[0], ChapterEntity):
                    prompt = prompt_builder.build_for_chapters(
                        results,
                        user_input
                    )
                elif isinstance(results[0], VerseTranslationEntity):
                    prompt = prompt_builder.build_for_verse_translations(
                        results,
                        user_input
                    )
                
                response = self.llm_collection.general.generate(prompt, 256)
                print("\n🧠 Jawaban:\n", response)
            
    def retrieve_user_input(self):
        return input("Masukkan prompt: ")
        