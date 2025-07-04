from fastapi import APIRouter, HTTPException
from app.infrastructure.http.controller.controller import Controller
from pydantic import BaseModel
from typing import List, Optional


class VerseTranslationResponse(BaseModel):
    """Response model for verse translation"""
    id: int
    content: str
    verse_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "Dhṛtarāṣṭra berkata: \"Wahai Sanjaya, apa yang dilakukan rakyatku dan para Pandawa, yang berkumpul di medan suci Kurukshetra, bersemangat untuk bertempur?\"",
                "verse_id": 1
            }
        }


class VerseResponse(BaseModel):
    """Response model for a single verse"""
    id: int
    verse_number: int
    text_hindi: str
    text_sanskrit: str
    text_sanskrit_meanings: str
    audio_url: str
    chapter_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "verse_number": 1,
                "text_hindi": "धृतराष्ट्र उवाच\n\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।\n",
                "text_sanskrit": "dhṛitarāśhtra uvācha\ndharma-kṣhetre kuru-kṣhetre samavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāśhchaiva kimakurvata sañjaya\n",
                "text_sanskrit_meanings": "dhṛitarāśhtraḥ uvācha—Dhritarashtra said; dharma-kṣhetre—the land of dharma; kuru-kṣhetre—at Kurukshetra; samavetāḥ—having gathered; yuyutsavaḥ—desiring to fight; māmakāḥ—my sons; pāṇḍavāḥ—the sons of Pandu; cha—and; eva—certainly; kim—what; akurvata—did they do; sañjaya—Sanjay\n",
                "audio_url": "https://gita.github.io/gita/data/verse_recitation/1/1.mp3",
                "chapter_id": 1
            }
        }


class VerseDetailResponse(BaseModel):
    """Response model for verse with translations"""
    id: int
    verse_number: int
    text_hindi: str
    text_sanskrit: str
    text_sanskrit_meanings: str
    audio_url: str
    chapter_id: int
    translations: List[VerseTranslationResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "verse_number": 1,
                "text_hindi": "धृतराष्ट्र उवाच\n\nधर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।\n\nमामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय।।1.1।।\n",
                "text_sanskrit": "dhṛitarāśhtra uvācha\ndharma-kṣhetre kuru-kṣhetre samavetā yuyutsavaḥ\nmāmakāḥ pāṇḍavāśhchaiva kimakurvata sañjaya\n",
                "text_sanskrit_meanings": "dhṛitarāśhtraḥ uvācha—Dhritarashtra said; dharma-kṣhetre—the land of dharma; kuru-kṣhetre—at Kurukshetra; samavetāḥ—having gathered; yuyutsavaḥ—desiring to fight; māmakāḥ—my sons; pāṇḍavāḥ—the sons of Pandu; cha—and; eva—certainly; kim—what; akurvata—did they do; sañjaya—Sanjay\n",
                "audio_url": "https://gita.github.io/gita/data/verse_recitation/1/1.mp3",
                "chapter_id": 1,
                "translations": [
                    {
                        "id": 1,
                        "content": "Dhṛtarāṣṭra berkata: \"Wahai Sanjaya, apa yang dilakukan rakyatku dan para Pandawa, yang berkumpul di medan suci Kurukshetra, bersemangat untuk bertempur?\"",
                        "verse_id": 1
                    },
                    {
                        "id": 2,
                        "content": "Dhritarashtra bertanya: \"Wahai Sanjaya, apa yang terjadi saat putra-putraku dan putra-putra Pandu berkumpul di tanah suci Kurukshetra, penuh gairah untuk bertempur?\"",
                        "verse_id": 1
                    }
                ]
            }
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


class VerseController(Controller):
    def __init__(self):
        self._router = APIRouter(
            prefix="/chapter",
            tags=["Verses"],
            responses={404: {"model": ErrorResponse}},
        )
        
        self._router.get(
            "/{chapter_number}/verse",
            response_model=List[VerseResponse],
            summary="Get all verses in a chapter",
            description="Retrieve all verses from a specific chapter with their Sanskrit text, Hindi text, meanings, and audio URLs.",
            response_description="List of verses in the specified chapter",
            responses={
                404: {
                    "description": "Chapter not found",
                    "model": ErrorResponse
                }
            }
        )(self.handle_verse_list)
        
        self._router.get(
            "/{chapter_number}/verse/{verse_number}",
            response_model=VerseDetailResponse,
            summary="Get specific verse with translations",
            description="Retrieve a specific verse by chapter and verse number, including all available translations.",
            response_description="Verse details with translations",
            responses={
                404: {
                    "description": "Verse not found",
                    "model": ErrorResponse
                }
            }
        )(self.handle_verse_detail)

    @property
    def router(self) -> APIRouter:
        return self._router

    async def handle_verse_list(self, chapter_number: int):
        """
        Get all verses from a specific chapter.
        
        Args:
            chapter_number (int): Chapter number (1-18)
            
        Returns:
            List[VerseResponse]: List of verses in the chapter
        """
        chapter_verses = self.ctx.verse_repository.get_by_chapter_number(chapter_number)
        return [x.to_dict() for x in chapter_verses]

    async def handle_verse_detail(self, chapter_number: int, verse_number: int):
        """
        Get a specific verse with all its translations.
        
        Args:
            chapter_number (int): Chapter number (1-18)
            verse_number (int): Verse number within the chapter
            
        Returns:
            VerseDetailResponse: Verse details with translations
            
        Raises:
            HTTPException: 404 if verse not found
        """
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
