from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.ai_math_controller import AIMathController
from src.schemas.ai_question_schema import GeneratedQuestionResponse
from src.schemas.ai_math_schema import GenerateMathQuestionRequest, MathTopicsResponse

ai_math_router = APIRouter()


@ai_math_router.get("/math/topics", response_model=MathTopicsResponse)
async def get_math_topics():
    return await AIMathController.get_math_topics()


@ai_math_router.post("/math", response_model=GeneratedQuestionResponse)
async def generate_math_question(
    request: GenerateMathQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await AIMathController.generate_math_question(request, db)
