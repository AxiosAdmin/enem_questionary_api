from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.question_schema import CreateQuestionRequest
from src.services.question_service import QuestionService


class QuestionController:
    @staticmethod
    async def create_question(
        request: CreateQuestionRequest,
        db: AsyncSession,
    ):
        try:
            return await QuestionService.create_question(request, db)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
