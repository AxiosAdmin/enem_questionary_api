from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.ai_natural_sciences_schema import (
    GenerateNaturalSciencesQuestionRequest,
)
from src.services.ai_natural_sciences_service import AINaturalSciencesService


class AINaturalSciencesController:
    @staticmethod
    async def get_natural_sciences_topics():
        return {"topics": AINaturalSciencesService.get_natural_sciences_topics()}

    @staticmethod
    async def generate_natural_sciences_question(
        request: GenerateNaturalSciencesQuestionRequest,
        db: AsyncSession,
    ):
        return await AINaturalSciencesService.generate_natural_sciences_question(
            request.topic, db
        )
