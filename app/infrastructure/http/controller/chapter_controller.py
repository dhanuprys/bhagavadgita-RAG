from fastapi import APIRouter, HTTPException
from app.infrastructure.http.controller.controller import Controller


class ChapterController(Controller):
    router = APIRouter()

    def __init__(self):
        self.router.get("/chapter")(self.handle_chapter)
        self.router.get("/chapter/{chapter_number}")(self.handle_chapter_by_number)

    async def handle_chapter(self):
        all_chapters = self.ctx.chapter_repository.get_all()
        return [x.to_dict() for x in all_chapters]

    async def handle_chapter_by_number(self, chapter_number: int):
        chapter = self.ctx.chapter_repository.get_chapter_by_number(chapter_number)

        if not chapter:
            raise HTTPException(status_code=404, detail="Item not found")

        return chapter.to_dict()
