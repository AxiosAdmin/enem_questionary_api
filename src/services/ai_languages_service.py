from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.languages_question import (
    build_enem_languages_question_prompt,
    build_random_languages_question_context,
    get_languages_topics,
    get_languages_topics_with_subtopics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AILanguagesService:
    @staticmethod
    def get_languages_topics():
        return get_languages_topics()

    @staticmethod
    def get_languages_topics_with_subtopics():
        return get_languages_topics_with_subtopics()

    @staticmethod
    async def generate_languages_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_languages_question_context,
            build_enem_languages_question_prompt,
            db,
        )
