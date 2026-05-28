from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.math_question import (
    build_enem_math_question_prompt,
    build_random_math_question_context,
    get_math_topics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AIMathService:
    @staticmethod
    def get_math_topics():
        return get_math_topics()

    @staticmethod
    async def generate_math_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_math_question_context,
            build_enem_math_question_prompt,
            db,
        )
