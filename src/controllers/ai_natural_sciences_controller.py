from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.ai_natural_sciences_schema import (
    GenerateNaturalSciencesQuestionRequest,
    GenerateNaturalSciencesQuestionWithSupportMaterialsRequest,
)
from src.services.ai_natural_sciences_service import AINaturalSciencesService


class AINaturalSciencesController:
    @staticmethod
    async def get_natural_sciences_topics():
        return {
            "topics": (
                AINaturalSciencesService.get_natural_sciences_topics_with_subtopics()
            )
        }

    @staticmethod
    async def generate_natural_sciences_question(
        request: GenerateNaturalSciencesQuestionRequest,
        db: AsyncSession,
    ):
        return await AINaturalSciencesService.generate_natural_sciences_question(
            request.topic, db
        )

    @staticmethod
    async def generate_natural_sciences_question_with_support_materials(
        request: GenerateNaturalSciencesQuestionWithSupportMaterialsRequest,
        db: AsyncSession,
    ):
        return await AINaturalSciencesService.generate_natural_sciences_question_with_support_materials(
            request.topic,
            request.support_material_ids,
            db,
        )
