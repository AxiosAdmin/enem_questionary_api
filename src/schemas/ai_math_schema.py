from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.helpers.math_question import get_math_topics


class MathSubtopicResponse(BaseModel):
    name: str
    description: str


class MathTopicResponse(BaseModel):
    topic: str
    subtopics: list[MathSubtopicResponse]


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


class GenerateMathQuestionWithSupportMaterialsRequest(GenerateMathQuestionRequest):
    support_material_ids: list[UUID] = Field(min_length=1)


class MathTopicsResponse(BaseModel):
    data: list[MathTopicResponse]
