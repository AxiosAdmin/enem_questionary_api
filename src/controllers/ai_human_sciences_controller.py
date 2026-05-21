from src.schemas.ai_human_sciences_schema import GenerateHumanSciencesQuestionRequest
from src.services.ai_human_sciences_service import AIHumanSciencesService


class AIHumanSciencesController:
    @staticmethod
    async def get_human_sciences_topics():
        return {"topics": AIHumanSciencesService.get_human_sciences_topics()}

    @staticmethod
    async def generate_human_sciences_question(
        request: GenerateHumanSciencesQuestionRequest,
    ):
        return AIHumanSciencesService.generate_human_sciences_question(request.topic)
