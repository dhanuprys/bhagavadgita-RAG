from rich import pretty
from rich.console import Console
from time import sleep

import app.domain.util.prompt_builder as prompt_builder
from app.application.application_construct import ApplicationConstruct
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult


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
                self.console.print(
                    f"[yellow][AI][/yellow] AI menemukan {len(results)} konteks terkait"
                )

                prompt = None
                if isinstance(results[0], ChapterEntity):
                    prompt = prompt_builder.build_for_chapters(results, user_input)
                elif isinstance(results[0], GitaEntity):
                    prompt = prompt_builder.build_for_gita(results, user_input)
                    i = 1
                    for ctx in results:
                        self.console.print(
                            f"[yellow][AI][/yellow][ctx] {i}. [b]Bab {ctx.c_chapter_number} sloka {ctx.v_verse_number}[/b]"
                        )
                        self.console.print(
                            f"[yellow][AI][/yellow][ctx]    {ctx.vt_content[:50]}..."
                        )
                        i += 1
                        sleep(0.5)

                self.console.print(
                    "[yellow][AI][/yellow] AI sedang merangkai kalimat yang sesuai"
                )
                response = self.app.llm_collection.general.generate_stream(prompt, 256)
                print()
                self.console.print("🚀 Jawaban berdasarkan konteks:")
                for chunk in response:
                    print(chunk.content_chunk, end="", flush=True)
                print("\n")

    def retrieve_user_input(self):
        return input(">> ")
