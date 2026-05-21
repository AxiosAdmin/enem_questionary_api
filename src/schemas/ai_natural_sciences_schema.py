from pydantic import BaseModel, field_validator

from src.helpers.natural_sciences_question import get_natural_sciences_topics


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


class NaturalSciencesTopicsResponse(BaseModel):
    topics: list[str]
