from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.ai_math_schema import GenerateMathQuestionRequest
from src.services.ai_math_service import AIMathService


class AIMathController:
    @staticmethod
    async def get_math_topics():
        return {"data": AIMathService.get_math_topics_with_subtopics()}

    @staticmethod
    async def generate_math_question(
        request: GenerateMathQuestionRequest,
        db: AsyncSession,
    ):
        return await AIMathService.generate_math_question(request.topic, db)
