from fastapi import APIRouter

from src.controllers.ai_natural_sciences_controller import AINaturalSciencesController
from src.schemas.ai_natural_sciences_schema import (
    GenerateNaturalSciencesQuestionRequest,
    NaturalSciencesTopicsResponse,
)

ai_natural_sciences_router = APIRouter()


@ai_natural_sciences_router.get(
    "/natural-sciences/topics", response_model=NaturalSciencesTopicsResponse
)
async def get_natural_sciences_topics():
    return await AINaturalSciencesController.get_natural_sciences_topics()


@ai_natural_sciences_router.post("/natural-sciences")
async def generate_natural_sciences_question(
    request: GenerateNaturalSciencesQuestionRequest,
):
    return await AINaturalSciencesController.generate_natural_sciences_question(request)
