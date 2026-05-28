from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.natural_sciences_question import (
    build_enem_natural_sciences_question_prompt,
    build_random_natural_sciences_question_context,
    get_natural_sciences_topics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AINaturalSciencesService:
    @staticmethod
    def get_natural_sciences_topics():
        return get_natural_sciences_topics()

    @staticmethod
    async def generate_natural_sciences_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_natural_sciences_question_context,
            build_enem_natural_sciences_question_prompt,
            db,
        )
