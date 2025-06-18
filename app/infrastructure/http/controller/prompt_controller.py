from fastapi import APIRouter
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.infrastructure.http.controller.controller import Controller
from pydantic import BaseModel
from rich.console import Console

router = APIRouter()


class PromptRequest(BaseModel):
    message: str


class PromptController(Controller):
    def __init__(self):
        router.post("/prompt")(self.handle_prompt)
        self.console = Console()

    def get_router(self):
        return router

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
            context_list = []
            if isinstance(results[0], ChapterEntity):
                prompt = self.ctx.prompt_builder.generate_chapter_prompt(
                    user_input, results
                )
            elif isinstance(results[0], GitaEntity) | isinstance(
                results[0], MixedGitaEntity
            ):
                flatten_context = []
                context_list = []
                for ctx in results:
                    if isinstance(ctx, GitaEntity):
                        flatten_context.append(ctx)
                        context_list.append(
                            {
                                "label": f"BG {ctx.c_chapter_number}.{ctx.v_verse_number}",
                                "content": f"\n\n*{ctx.v_text_sanskrit.strip()}*\n\n{ctx.vt_content.strip()}",
                            }
                        )
                    if isinstance(ctx, MixedGitaEntity):
                        labels = []
                        content = []
                        for g in ctx.gita:
                            flatten_context.append(g)
                            labels.append(f"BG {g.c_chapter_number}.{g.v_verse_number}")
                            content.append(
                                f"\n\n*{g.v_text_sanskrit.strip()}*\n\n{g.vt_content.strip()}"
                            )

                        context_list.append(
                            {
                                "label": ", ".join(labels),
                                "content": "\n\n".join(content),
                            }
                        )

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
            return {"context": context_list, "answer": c}
