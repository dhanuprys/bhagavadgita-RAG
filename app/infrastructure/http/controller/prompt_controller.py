from fastapi import APIRouter
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.infrastructure.http.controller.controller import Controller
from pydantic import BaseModel
from rich.console import Console
from os import getenv


class PromptRequest(BaseModel):
    message: str


class PromptController(Controller):
    router = APIRouter()
    library_base_url = getenv("LIBRARY_BASE_URL") or "http://localhost:5173"

    def __init__(self):
        self.router.post("/prompt")(self.handle_prompt)
        self.console = Console()

    async def handle_prompt(self, request: PromptRequest):
        user_input = request.message
        results = self.app.get_context(user_input)

        if not results or len(results) <= 0:
            return {"context": [], "answer": "Pertanyaan anda tidak sesuai konteks."}

        if isinstance(results, PatternMatchingResult):
            print(results.output)
        else:
            self.console.print(
                f"[yellow][AI][/yellow] AI menemukan {len(results)} konteks terkait"
            )

            prompt = None
            context_type = ""
            flatten_context = []
            context_list = []
            seen_context = []
            links = []
            if isinstance(results[0], ChapterEntity):
                context_type = "chapter"
                prompt = self.ctx.prompt_builder.generate_chapter_prompt(
                    user_input, results
                )
            elif isinstance(results[0], GitaEntity) | isinstance(
                results[0], MixedGitaEntity
            ):
                context_type = "verse"
                for ctx in results:
                    if isinstance(ctx, GitaEntity):
                        context_label = (
                            f"BG {ctx.c_chapter_number}.{ctx.v_verse_number}"
                        )
                        if context_label in seen_context:
                            continue

                        seen_context.append(context_label)
                        flatten_context.append(ctx)
                        context_list.append(
                            {
                                "label": context_label,
                                "content": f"\n\n*{ctx.v_text_sanskrit.strip()}*\n\n{ctx.vt_content.strip()}",
                                "link": f"{self.library_base_url}/chapter/{ctx.c_chapter_number}/verse/{ctx.v_verse_number}",
                            }
                        )
                    if isinstance(ctx, MixedGitaEntity):
                        i = 0
                        for g in ctx.gita:
                            context_label = (
                                f"BG {g.c_chapter_number}.{g.v_verse_number} (m{i})"
                            )

                            if context_label in seen_context:
                                continue

                            seen_context.append(context_label)

                            flatten_context.append(g)

                            context_list.append(
                                {
                                    "label": context_label,
                                    "content": f"\n\n*{g.v_text_sanskrit.strip()}*\n\n{g.vt_content.strip()}",
                                    "link": f"{self.library_base_url}/chapter/{g.c_chapter_number}/verse/{g.v_verse_number}",
                                }
                            )
                        i += 1

                prompt = self.ctx.prompt_builder.generate_global_gita_prompt(
                    user_input,
                    flatten_context,
                )

            self.console.print(
                "[yellow][AI][/yellow] AI sedang merangkai kalimat yang sesuai"
            )
            response = self.ctx.llm_collection.general.generate_stream(prompt, 256)
            c = ""
            for chunk in response:
                c += chunk.content_chunk

            return {
                "context": context_list,
                "context_type": context_type,
                "answer": c,
            }
