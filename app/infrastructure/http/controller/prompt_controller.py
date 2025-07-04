from dataclasses import dataclass, field
from typing import List, Literal
from fastapi import APIRouter
from app.domain.entity.gita_entity import GitaEntity, MixedGitaEntity
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.domain.value_object.attachment import Attachment
from app.infrastructure.http.controller.controller import Controller
from pydantic import BaseModel
from rich.console import Console
from os import getenv
import random
import time


@dataclass
class ChatContext:
    label: str
    content: str
    link: str | None = None

    def to_dict(self):
        return {
            "label": self.label,
            "content": self.content,
            "link": self.link,
        }


@dataclass
class ChatResponse:
    answer: str = ""
    context: List[ChatContext] = field(default_factory=list)
    answer_system: Literal["intent", "semantic"] = "intent"
    suggestions: List[str] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)

    def to_dict(self):
        return {
            "answer": self.answer,
            "context": [x.to_dict() for x in self.context],
            "answer_system": self.answer_system,
            "suggestions": self.suggestions,
            "attachments": [x.to_dict() for x in self.attachments],
        }


class PromptRequest(BaseModel):
    message: str


class PromptController(Controller):
    library_base_url = getenv("LIBRARY_BASE_URL") or "http://localhost:5173"

    def __init__(self):
        self._router = APIRouter()
        self._router.post("/prompt")(self.handle_prompt)
        self._router.get("/suggestions")(self.handle_random_suggestions)
        self.console = Console()

    @property
    def router(self):
        return self._router

    def get_random_suggestions(self) -> List[str]:
        suggestions = [
            # Kategori: get_specific_verse (Permintaan Sloka Spesifik)
            "Tolong berikan isi dari Bhagavad Gita bab 2 sloka 47.",  # Formal
            "apa kata sloka 18.66?",  # Lebih santai
            "Gita 7.7",  # Format singkat
            "Saya ingin membaca ayat ke-34 dari bab 4.",  # Variasi kata 'ayat'
            "tampilkan bhagawad gita 9.22 untuk saya",  # Variasi penulisan
            "apa isi dari sloka pertama di bab pertama?",  # Menggunakan kata relatif 'pertama'
            # Kategori: get_random_verses (Permintaan Sloka Acak)
            "berikan saya satu sloka acak untuk direnungkan hari ini",
            "kasih 5 sloka bebas dari mana saja",
            "butuh kutipan inspiratif dari Gita",  # Implisit meminta sloka acak
            "tampilkan 3 sloka secara random",
            # Kategori: get_sample_verses (Permintaan Sampel Sloka dari Bab Tertentu)
            "sebutkan 4 sloka dari bab 11",  # expandable: false
            "berikan 2 contoh ayat dari bab 13",  # expandable: false
            "tampilkan 3 sloka pembuka dari bab 1",  # expandable: false
            "apa saja sloka-sloka penting pada bab 12?",  # expandable: true
            "beberapa ayat dari bab 15 dong",  # expandable: true
            "tunjukkan isi dari bab 6",  # expandable: true, frasa ambigu
            # Kategori: get_chapter_summary (Permintaan Ringkasan Bab)
            "buatkan ringkasan untuk bab 10",
            "ceritakan tentang bab 2",  # Gaya bahasa naratif
            "Bab 7 itu intinya tentang apa?",
            "Bab 18",  # Permintaan implisit untuk ringkasan
            "jelaskan secara singkat isi dari bab lima",  # Variasi
            # Kategori: get_chapter_metadata (Permintaan Info Tentang Bab)
            "ada berapa total sloka di bab 15?",  # Metadata: verse_count
            "apa judul dari bab 8?",  # Metadata: chapter_name
            "Bab 11 punya berapa ayat?",  # Metadata: verse_count
            "sebutkan nama lain dari bab 1",  # Metadata: chapter_name
        ]

        random.shuffle(suggestions)
        return suggestions[:4]

    async def handle_random_suggestions(self):
        return {"suggestions": self.get_random_suggestions()}

    async def handle_prompt(self, request: PromptRequest):
        chat_response = ChatResponse()
        chat_response.suggestions = self.get_random_suggestions()

        user_input = request.message
        # perf
        start_time = time.perf_counter()
        results = self.app.get_context(user_input)
        end_time = time.perf_counter()
        time_duration = end_time - start_time
        print(f"Took {time_duration:.3f} seconds")

        self.console.print(f"[red][PROMPT][/red] {user_input}")

        if not results or (isinstance(results, list) and len(results) <= 0):
            chat_response.answer = "Pertanyaan anda tidak sesuai konteks."
            return chat_response.to_dict()

        ##############################################################################
        if isinstance(results, PatternMatchingResult):
            chat_response.answer_system = "intent"

            if results.type == "context":
                flatten_pattern_context: List[str] = []
                seen_pattern_context: List[str] = []
                for ctx in results.context:
                    if ctx.label in seen_pattern_context:
                        continue

                    seen_pattern_context.append(ctx.label)
                    flatten_pattern_context.append(ctx.content)
                    chat_response.context.append(
                        ChatContext(
                            label=ctx.label,
                            content=ctx.display_content,
                            link=ctx.link,
                        )
                    )
                    chat_response.attachments.extend(ctx.attachments)

                prompt = self.ctx.prompt_builder.generate_flexible_prompt(
                    user_input,
                    flatten_pattern_context,
                )

                # perf
                start_time = time.perf_counter()
                response = self.ctx.llm_collection.general.generate_stream(prompt, 256)
                for chunk in response:
                    chat_response.answer += chunk.content_chunk
                end_time = time.perf_counter()
                time_duration = end_time - start_time
                print(f"Took (generation) {time_duration:.3f} seconds")
            elif results.type == "direct":
                chat_response.answer = results.output
        if isinstance(results, list):
            chat_response.answer_system = "semantic"

            self.console.print(
                f"[yellow][AI][/yellow] AI menemukan {len(results)} konteks terkait"
            )

            prompt = None
            flatten_context: List[GitaEntity] = []
            seen_context: List[str] = []

            for ctx in results:
                if isinstance(ctx, GitaEntity):
                    context_label = f"BG {ctx.c_chapter_number}.{ctx.v_verse_number}"
                    if context_label in seen_context:
                        continue

                    seen_context.append(context_label)
                    flatten_context.append(ctx)

                    chat_response.context.append(
                        ChatContext(
                            label=context_label,
                            content=f"\n\n*{ctx.v_text_sanskrit.strip()}*\n\n{ctx.vt_content.strip()}",
                            link=f"{self.library_base_url}/chapter/{ctx.c_chapter_number}/verse/{ctx.v_verse_number}",
                        )
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
                        chat_response.context.append(
                            ChatContext(
                                label=context_label,
                                content=f"\n\n*{g.v_text_sanskrit.strip()}*\n\n{g.vt_content.strip()}",
                                link=f"{self.library_base_url}/chapter/{g.c_chapter_number}/verse/{g.v_verse_number}",
                            )
                        )
                    i += 1

            prompt = self.ctx.prompt_builder.generate_global_gita_prompt(
                user_input,
                flatten_context,
            )

            self.console.print(
                "[yellow][AI][/yellow] AI sedang merangkai kalimat yang sesuai"
            )
            # perf
            start_time = time.perf_counter()
            response = self.ctx.llm_collection.general.generate_stream(prompt, 256)

            for chunk in response:
                chat_response.answer += chunk.content_chunk
            end_time = time.perf_counter()
            time_duration = end_time - start_time
            print(f"Took (generation#2) {time_duration:.3f} seconds")

        return chat_response.to_dict()
