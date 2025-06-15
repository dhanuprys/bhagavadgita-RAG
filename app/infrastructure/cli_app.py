from app.application.application_construct import ApplicationConstruct
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.verse_translation_entity import VerseTranslationEntity
import app.domain.util.prompt_builder as prompt_builder
from rich import pretty
from rich.console import Console

class CLIApp(ApplicationConstruct):
    def run(self):
        pretty.install()
        self.console = Console()
        
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
                
                self.console.print(f"[yellow][AI][/yellow] AI menemukan {len(results)} konteks terkait")
                
                self.console.print("[yellow][AI][/yellow] AI sedang merangkai kalimat yang sesuai")
                response = self.llm_collection.general.generate_stream(prompt, 256)
                print()
                self.console.print('🚀 Jawaban berdasarkan konteks:')
                for chunk in response:
                    print(chunk.content_chunk, end="", flush=True)
                print("\n")
            
    def retrieve_user_input(self):
        return input(">> ")
        