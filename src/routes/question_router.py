from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.configs.db_connection import get_db
from src.controllers.question_controller import QuestionController
from src.schemas.question_schema import CreateQuestionRequest, CreateQuestionResponse

question_router = APIRouter()


@question_router.post(
    "/questions",
    response_model=CreateQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_question(
    request: CreateQuestionRequest,
    db: AsyncSession = Depends(get_db),
):
    return await QuestionController.create_question(request, db)
