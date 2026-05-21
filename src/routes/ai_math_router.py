from fastapi import APIRouter

from src.controllers.ai_math_controller import AIMathController
from src.schemas.ai_math_schema import GenerateMathQuestionRequest, MathTopicsResponse

ai_math_router = APIRouter()


@ai_math_router.get("/math/topics", response_model=MathTopicsResponse)
async def get_math_topics():
    return await AIMathController.get_math_topics()


@ai_math_router.post("/math")
async def generate_math_question(request: GenerateMathQuestionRequest):
    return await AIMathController.generate_math_question(request)
