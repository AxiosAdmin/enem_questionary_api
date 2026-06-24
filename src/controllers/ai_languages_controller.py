from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.ai_languages_schema import (
    GenerateLanguagesQuestionRequest,
    GenerateLanguagesQuestionWithSupportMaterialsRequest,
)
from src.services.ai_languages_service import AILanguagesService


class AILanguagesController:
    @staticmethod
    async def get_languages_topics():
        return {"topics": AILanguagesService.get_languages_topics_with_subtopics()}

    @staticmethod
    async def generate_languages_question(
        request: GenerateLanguagesQuestionRequest,
        db: AsyncSession,
    ):
        return await AILanguagesService.generate_languages_question(request.topic, db)

    @staticmethod
    async def generate_languages_question_with_support_materials(
        request: GenerateLanguagesQuestionWithSupportMaterialsRequest,
        db: AsyncSession,
    ):
        return await AILanguagesService.generate_languages_question_with_support_materials(
            request.topic,
            request.support_material_ids,
            db,
        )
