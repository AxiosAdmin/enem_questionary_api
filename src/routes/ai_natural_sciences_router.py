from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.ai_natural_sciences_controller import AINaturalSciencesController
from src.schemas.ai_question_schema import GeneratedQuestionResponse
from src.schemas.ai_natural_sciences_schema import (
    GenerateNaturalSciencesQuestionRequest,
    GenerateNaturalSciencesQuestionWithSupportMaterialsRequest,
    NaturalSciencesTopicsResponse,
)

ai_natural_sciences_router = APIRouter()


@ai_natural_sciences_router.get(
    "/natural-sciences/topics", response_model=NaturalSciencesTopicsResponse
)
async def get_natural_sciences_topics():
    return await AINaturalSciencesController.get_natural_sciences_topics()


@ai_natural_sciences_router.post(
    "/natural-sciences", response_model=GeneratedQuestionResponse
)
async def generate_natural_sciences_question(
    request: GenerateNaturalSciencesQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AINaturalSciencesController.generate_natural_sciences_question(
        request, db
    )


@ai_natural_sciences_router.post(
    "/natural-sciences/with-support-materials",
    response_model=GeneratedQuestionResponse,
)
async def generate_natural_sciences_question_with_support_materials(
    request: GenerateNaturalSciencesQuestionWithSupportMaterialsRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AINaturalSciencesController.generate_natural_sciences_question_with_support_materials(
        request, db
    )
