from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.natural_sciences_question import (
    build_enem_natural_sciences_question_prompt,
    build_random_natural_sciences_question_context,
    get_natural_sciences_topics,
    get_natural_sciences_topics_with_subtopics,
)
from src.services.enem_question_generation_service import (
    generate_enem_question,
    generate_enem_question_with_support_materials,
)


class AINaturalSciencesService:
    @staticmethod
    def get_natural_sciences_topics():
        return get_natural_sciences_topics()

    @staticmethod
    def get_natural_sciences_topics_with_subtopics():
        return get_natural_sciences_topics_with_subtopics()

    @staticmethod
    async def generate_natural_sciences_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_natural_sciences_question_context,
            build_enem_natural_sciences_question_prompt,
            db,
        )

    @staticmethod
    async def generate_natural_sciences_question_with_support_materials(
        topic: str,
        support_material_ids: list,
        db: AsyncSession,
    ):
        return await generate_enem_question_with_support_materials(
            topic,
            support_material_ids,
            build_random_natural_sciences_question_context,
            build_enem_natural_sciences_question_prompt,
            db,
        )
