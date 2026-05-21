from fastapi import APIRouter

from src.controllers.ai_languages_controller import AILanguagesController
from src.schemas.ai_languages_schema import (
    GenerateLanguagesQuestionRequest,
    LanguagesTopicsResponse,
)

ai_languages_router = APIRouter()


@ai_languages_router.get("/languages/topics", response_model=LanguagesTopicsResponse)
async def get_languages_topics():
    return await AILanguagesController.get_languages_topics()


@ai_languages_router.post("/languages")
async def generate_languages_question(request: GenerateLanguagesQuestionRequest):
    return await AILanguagesController.generate_languages_question(request)
