from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.ai_languages_controller import AILanguagesController
from src.schemas.ai_question_schema import GeneratedQuestionResponse
from src.schemas.ai_languages_schema import (
    GenerateLanguagesQuestionRequest,
    GenerateLanguagesQuestionWithSupportMaterialsRequest,
    LanguagesTopicsResponse,
)

ai_languages_router = APIRouter()


@ai_languages_router.get("/languages/topics", response_model=LanguagesTopicsResponse)
async def get_languages_topics():
    return await AILanguagesController.get_languages_topics()


@ai_languages_router.post("/languages", response_model=GeneratedQuestionResponse)
async def generate_languages_question(
    request: GenerateLanguagesQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AILanguagesController.generate_languages_question(request, db)


@ai_languages_router.post(
    "/languages/with-support-materials",
    response_model=GeneratedQuestionResponse,
)
async def generate_languages_question_with_support_materials(
    request: GenerateLanguagesQuestionWithSupportMaterialsRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AILanguagesController.generate_languages_question_with_support_materials(
        request, db
    )
