from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.human_sciences_question import (
    build_enem_human_sciences_question_prompt,
    build_random_human_sciences_question_context,
    get_human_sciences_topics,
    get_human_sciences_topics_with_subtopics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AIHumanSciencesService:
    @staticmethod
    def get_human_sciences_topics():
        return get_human_sciences_topics()

    @staticmethod
    def get_human_sciences_topics_with_subtopics():
        return get_human_sciences_topics_with_subtopics()

    @staticmethod
    async def generate_human_sciences_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_human_sciences_question_context,
            build_enem_human_sciences_question_prompt,
            db,
        )
