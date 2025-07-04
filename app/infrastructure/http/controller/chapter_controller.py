from fastapi import APIRouter, HTTPException
from app.infrastructure.http.controller.controller import Controller
from pydantic import BaseModel, RootModel
from typing import List, Optional
from fastapi.responses import JSONResponse


class ChapterResponse(BaseModel):
    """Response model for a single chapter"""
    id: int
    chapter_number: int
    name: str
    name_hindi: str
    name_sanskrit: str
    summary: str
    verses_count: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "chapter_number": 1,
                "name": "Dilema Arjuna",
                "name_hindi": "अर्जुनविषादयोग",
                "name_sanskrit": "Arjun Viṣhād Yog",
                "summary": "Bab pertama Bhagavad Gita - \"Arjuna Vishada Yoga\" memperkenalkan latar belakang, pengaturan, karakter, dan keadaan yang menyebabkan pertempuran epik Mahabharata, yang diperjuangkan antara Pandawa dan Kurawa. Bab ini menguraikan alasan-alasan yang menyebabkan terungkapnya Bhagavad Gita.\nSaat kedua pasukan berdiri siap untuk pertempuran, prajurit perkasa Arjuna, saat mengamati para prajurit di kedua belah pihak, menjadi semakin sedih dan tertekan karena ketakutan kehilangan kerabat dan teman-temannya serta dosa-dosa yang diakibatkan oleh pembunuhan kerabatnya sendiri. Maka, ia menyerah kepada Dewa Krishna, mencari solusi. Demikianlah, muncullah kebijaksanaan Bhagavad Gita.",
                "verses_count": 47
            }
        }


class ChapterListResponse(RootModel[List[ChapterResponse]]):
    """Response model for list of chapters"""
    
    class Config:
        json_schema_extra = {
            "example": [
                {
                    "id": 1,
                    "chapter_number": 1,
                    "name": "Dilema Arjuna",
                    "name_hindi": "अर्जुनविषादयोग",
                    "name_sanskrit": "Arjun Viṣhād Yog",
                    "summary": "Bab pertama Bhagavad Gita - \"Arjuna Vishada Yoga\" memperkenalkan latar belakang, pengaturan, karakter, dan keadaan yang menyebabkan pertempuran epik Mahabharata, yang diperjuangkan antara Pandawa dan Kurawa. Bab ini menguraikan alasan-alasan yang menyebabkan terungkapnya Bhagavad Gita.\nSaat kedua pasukan berdiri siap untuk pertempuran, prajurit perkasa Arjuna, saat mengamati para prajurit di kedua belah pihak, menjadi semakin sedih dan tertekan karena ketakutan kehilangan kerabat dan teman-temannya serta dosa-dosa yang diakibatkan oleh pembunuhan kerabatnya sendiri. Maka, ia menyerah kepada Dewa Krishna, mencari solusi. Demikianlah, muncullah kebijaksanaan Bhagavad Gita.",
                    "verses_count": 47
                },
                {
                    "id": 2,
                    "chapter_number": 2,
                    "name": "Pengetahuan Transendental",
                    "name_hindi": "सांख्ययोग",
                    "name_sanskrit": "Sānkhya Yog",
                    "summary": "Bab kedua Bhagavad Gita adalah \"Sankhya Yoga\". Ini adalah bab terpenting Bhagavad Gita karena Dewa Krishna memadatkan ajaran seluruh Gita dalam bab ini. Bab ini adalah esensi dari seluruh Gita.",
                    "verses_count": 72
                }
            ]
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Item not found"
            }
        }


class ChapterController(Controller):
    def __init__(self):
        self._router = APIRouter(
            prefix="/chapter",
            tags=["Chapters"],
            responses={404: {"model": ErrorResponse}},
        )
        
        self._router.get(
            "",
            response_model=List[ChapterResponse],
            summary="Get all chapters",
            description="Retrieve all 18 chapters of the Bhagavad Gita with their metadata including names in multiple languages, summaries, and verse counts.",
            response_description="List of all Bhagavad Gita chapters"
        )(self.handle_chapter)
        
        self._router.get(
            "/{chapter_number}",
            response_model=ChapterResponse,
            summary="Get chapter by number",
            description="Retrieve a specific chapter by its number (1-18) with complete metadata including Sanskrit and Hindi names, summary, and verse count.",
            response_description="Chapter details for the specified chapter number",
            responses={
                404: {
                    "description": "Chapter not found",
                    "model": ErrorResponse
                }
            }
        )(self.handle_chapter_by_number)

    @property
    def router(self) -> APIRouter:
        return self._router

    async def handle_chapter(self):
        """
        Get all chapters of the Bhagavad Gita.
        
        Returns:
            List[ChapterResponse]: List of all 18 chapters with their metadata
        """
        all_chapters = self.ctx.chapter_repository.get_all()
        return [x.to_dict() for x in all_chapters]

    async def handle_chapter_by_number(self, chapter_number: int):
        """
        Get a specific chapter by its number.
        
        Args:
            chapter_number (int): Chapter number (1-18)
            
        Returns:
            ChapterResponse: Chapter details
            
        Raises:
            HTTPException: 404 if chapter not found
        """
        chapter = self.ctx.chapter_repository.get_chapter_by_number(chapter_number)

        if not chapter:
            raise HTTPException(status_code=404, detail="Item not found")

        return chapter.to_dict()
