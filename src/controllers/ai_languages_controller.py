from src.schemas.ai_languages_schema import GenerateLanguagesQuestionRequest
from src.services.ai_languages_service import AILanguagesService


class AILanguagesController:
    @staticmethod
    async def get_languages_topics():
        return {"topics": AILanguagesService.get_languages_topics()}

    @staticmethod
    async def generate_languages_question(request: GenerateLanguagesQuestionRequest):
        return AILanguagesService.generate_languages_question(request.topic)
