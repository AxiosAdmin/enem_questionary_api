from src.helpers.languages_question import (
    build_enem_languages_question_prompt,
    build_random_languages_question_context,
    get_languages_topics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AILanguagesService:
    @staticmethod
    def get_languages_topics():
        return get_languages_topics()

    @staticmethod
    def generate_languages_question(topic: str):
        return generate_enem_question(
            topic,
            build_random_languages_question_context,
            build_enem_languages_question_prompt,
        )
