from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.helpers.languages_question import get_languages_topics


class LanguagesSubtopicResponse(BaseModel):
    name: str
    description: str


class LanguagesTopicResponse(BaseModel):
    topic: str
    subtopics: list[LanguagesSubtopicResponse]


class GenerateLanguagesQuestionRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        if value not in get_languages_topics():
            raise ValueError(
                f"Invalid topic. Supported topics are: {', '.join(get_languages_topics())}"
            )
        return value


class GenerateLanguagesQuestionWithSupportMaterialsRequest(
    GenerateLanguagesQuestionRequest
):
    support_material_ids: list[UUID] = Field(min_length=1)


class LanguagesTopicsResponse(BaseModel):
    topics: list[LanguagesTopicResponse]
