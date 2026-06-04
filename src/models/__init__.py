from typing import Any
from src.models.models import (
    Coupons,
    CouponRedemptions,
    Profiles,
    QuestionAssets,
    Questions,
    QuestionAnswers,
    QuestionFeedbacks,
    Subscriptions,
    UserFeedback,
    Users,
)
from src.schemas.ai_question_schema import GeneratedQuestionGeneric
from src.configs.db_connection import get_db

routes: list[dict[str, Any]] = [
    {
        "model_class": Questions,
        "standard_schema": GeneratedQuestionGeneric,
        "db_session": get_db,
        "auth_callback": None,
        "request_post_schema": None,
        "request_patch_schema": None,
        "response_get_schema": None,
        "response_get_by_id_schema": None,
        "response_post_schema": None,
        "response_delete_schema": None,
        "response_patch_schema": None,
        "use_get": False,
        "use_get_by_id": False,
        "use_post": True,
        "use_delete": False,
        "use_patch": False,
        "join_parameters": None,
        "second_level_join_parameters": None,
        "route_prefix": "/questions",
        "route_tags": ["Questions"],
        "dependencies": True,
    },
]
