from fastapi import APIRouter

from src.controllers.ai_human_sciences_controller import AIHumanSciencesController
from src.schemas.ai_human_sciences_schema import (
    GenerateHumanSciencesQuestionRequest,
    HumanSciencesTopicsResponse,
)

ai_human_sciences_router = APIRouter()


@ai_human_sciences_router.get(
    "/human-sciences/topics", response_model=HumanSciencesTopicsResponse
)
async def get_human_sciences_topics():
    return await AIHumanSciencesController.get_human_sciences_topics()


@ai_human_sciences_router.post("/human-sciences")
async def generate_human_sciences_question(
    request: GenerateHumanSciencesQuestionRequest,
):
    return await AIHumanSciencesController.generate_human_sciences_question(request)
