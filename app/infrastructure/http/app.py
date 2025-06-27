from rich import pretty
from rich.console import Console
from time import sleep
from typing import List

from app.application.application_construct import ApplicationConstruct
from app.domain.entity.chapter_entity import ChapterEntity
from app.domain.entity.gita_entity import GitaEntity
from app.domain.value_object.pattern_matching_result import PatternMatchingResult
from app.infrastructure.http.controller.controller import Controller
from app.infrastructure.http.controller.prompt_controller import PromptController
from app.infrastructure.http.controller.chapter_controller import ChapterController
from app.infrastructure.http.controller.verse_controller import VerseController
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class HttpApp(ApplicationConstruct):
    def run(self):
        pretty.install()
        self.console = Console()

        self.prepare_model()
        self.http = FastAPI()

        self.register_routes()
        self.start_server()

    def register_routes(self):
        self.http.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        controllers: List[Controller] = [
            ChapterController(),
            PromptController(),
            VerseController(),
        ]

        for c in controllers:
            c.set_app(self, self.app)
            self.http.include_router(c.router)

    def start_server(self):
        import uvicorn

        uvicorn.run(self.http, host="0.0.0.0")
