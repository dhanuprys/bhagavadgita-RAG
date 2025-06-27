from fastapi import APIRouter, HTTPException
from app.infrastructure.http.controller.controller import Controller


class VerseController(Controller):
    router = APIRouter()

    def __init__(self):
        self.router.get("/chapter/{chapter_number}/verse")(self.handle_verse_list)
        self.router.get("/chapter/{chapter_number}/verse/{verse_number}")(
            self.handle_verse_detail
        )

    async def handle_verse_list(self, chapter_number: int):
        chapter_verses = self.ctx.verse_repository.get_by_chapter_number(chapter_number)
        return [x.to_dict() for x in chapter_verses]

    async def handle_verse_detail(self, chapter_number: int, verse_number: int):
        verse_detail = self.ctx.verse_repository.get_by_chapter_verse_number(
            chapter_number,
            verse_number,
        )

        if not verse_detail:
            raise HTTPException(status_code=404, detail="Item not found")

        translation = self.ctx.verse_translation_repository.get_by_verse_id(
            verse_detail.id
        )

        return {
            **verse_detail.to_dict(),
            "translations": [x.to_dict() for x in translation],
        }
