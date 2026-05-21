from src.helpers.human_sciences_question import (
    build_enem_human_sciences_question_prompt,
    build_random_human_sciences_question_context,
    get_human_sciences_topics,
)
from src.services.enem_question_generation_service import generate_enem_question


class AIHumanSciencesService:
    @staticmethod
    def get_human_sciences_topics():
        return get_human_sciences_topics()

    @staticmethod
    def generate_human_sciences_question(topic: str):
        return generate_enem_question(
            topic,
            build_random_human_sciences_question_context,
            build_enem_human_sciences_question_prompt,
        )
