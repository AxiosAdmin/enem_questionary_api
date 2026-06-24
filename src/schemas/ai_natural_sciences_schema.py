from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from src.helpers.natural_sciences_question import get_natural_sciences_topics


class NaturalSciencesSubtopicResponse(BaseModel):
    name: str
    description: str


class NaturalSciencesTopicResponse(BaseModel):
    topic: str
    subtopics: list[NaturalSciencesSubtopicResponse]


class GenerateNaturalSciencesQuestionRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        if value not in get_natural_sciences_topics():
            raise ValueError(
                "Invalid topic. Supported topics are: "
                f"{', '.join(get_natural_sciences_topics())}"
            )
        return value


class GenerateNaturalSciencesQuestionWithSupportMaterialsRequest(
    GenerateNaturalSciencesQuestionRequest
):
    support_material_ids: list[UUID] = Field(min_length=1)


class NaturalSciencesTopicsResponse(BaseModel):
    topics: list[NaturalSciencesTopicResponse]
