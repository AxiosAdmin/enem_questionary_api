from pydantic import BaseModel, field_validator

from src.helpers.math_question import get_math_topics


class GenerateMathQuestionRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        if value not in get_math_topics():
            raise ValueError(
                f"Invalid topic. Supported topics are: {', '.join(get_math_topics())}"
            )
        return value


class MathTopicsResponse(BaseModel):
    data: list[str]
