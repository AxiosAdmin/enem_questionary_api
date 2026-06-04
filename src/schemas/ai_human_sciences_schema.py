from pydantic import BaseModel, field_validator

from src.helpers.human_sciences_question import get_human_sciences_topics


class HumanSciencesSubtopicResponse(BaseModel):
    name: str
    description: str


class HumanSciencesTopicResponse(BaseModel):
    topic: str
    subtopics: list[HumanSciencesSubtopicResponse]


class GenerateHumanSciencesQuestionRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value: str) -> str:
        if value not in get_human_sciences_topics():
            raise ValueError(
                f"Invalid topic. Supported topics are: {', '.join(get_human_sciences_topics())}"
            )
        return value


class HumanSciencesTopicsResponse(BaseModel):
    topics: list[HumanSciencesTopicResponse]
