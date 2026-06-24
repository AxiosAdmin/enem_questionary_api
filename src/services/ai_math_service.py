from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.math_question import (
    build_enem_math_question_prompt,
    build_random_math_question_context,
    get_math_topics,
    get_math_topics_with_subtopics,
)
from src.services.enem_question_generation_service import (
    generate_enem_question,
    generate_enem_question_with_support_materials,
)


class AIMathService:
    @staticmethod
    def get_math_topics():
        return get_math_topics()

    @staticmethod
    def get_math_topics_with_subtopics():
        return get_math_topics_with_subtopics()

    @staticmethod
    async def generate_math_question(topic: str, db: AsyncSession):
        return await generate_enem_question(
            topic,
            build_random_math_question_context,
            build_enem_math_question_prompt,
            db,
        )

    @staticmethod
    async def generate_math_question_with_support_materials(
        topic: str,
        support_material_ids: list,
        db: AsyncSession,
    ):
        return await generate_enem_question_with_support_materials(
            topic,
            support_material_ids,
            build_random_math_question_context,
            build_enem_math_question_prompt,
            db,
        )
