from src.routes.auth_router import auth_router
from src.routes.ai_math_router import ai_math_router
from src.routes.ai_languages_router import ai_languages_router
from src.routes.ai_natural_sciences_router import ai_natural_sciences_router
from src.routes.ai_human_sciences_router import ai_human_sciences_router
from src.routes.question_router import question_router

__all__ = [
    "auth_router",
    "question_router",
    "ai_math_router",
    "ai_languages_router",
    "ai_natural_sciences_router",
    "ai_human_sciences_router",
]
