from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.ai_human_sciences_controller import AIHumanSciencesController
from src.schemas.ai_question_schema import GeneratedQuestionResponse
from src.schemas.ai_human_sciences_schema import (
    GenerateHumanSciencesQuestionRequest,
    GenerateHumanSciencesQuestionWithSupportMaterialsRequest,
    HumanSciencesTopicsResponse,
)

ai_human_sciences_router = APIRouter()


@ai_human_sciences_router.get(
    "/human-sciences/topics", response_model=HumanSciencesTopicsResponse
)
async def get_human_sciences_topics():
    return await AIHumanSciencesController.get_human_sciences_topics()


@ai_human_sciences_router.post(
    "/human-sciences", response_model=GeneratedQuestionResponse
)
async def generate_human_sciences_question(
    request: GenerateHumanSciencesQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AIHumanSciencesController.generate_human_sciences_question(request, db)


@ai_human_sciences_router.post(
    "/human-sciences/with-support-materials",
    response_model=GeneratedQuestionResponse,
)
async def generate_human_sciences_question_with_support_materials(
    request: GenerateHumanSciencesQuestionWithSupportMaterialsRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AIHumanSciencesController.generate_human_sciences_question_with_support_materials(
        request, db
    )
