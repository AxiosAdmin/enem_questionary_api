from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class QuestionSupportMaterialResponse(BaseModel):
    id: UUID
    asset_type: str
    rendering_mode: str
    position: str
    display_order: int
    storage_status: str
    title: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    source_label: str | None = None
    content: str | None = None
    storage_provider: str | None = None
    storage_key: str | None = None
    public_url: str | None = None
    mime_type: str | None = None
    data: dict[str, Any] | None = None


class GeneratedQuestionResponse(BaseModel):
    id: UUID
    topic: str
    subtopic: str
    subtopic_description: str
    diversity_mode: str
    question: str
    answer_a: str
    answer_b: str
    answer_c: str
    answer_d: str
    answer_e: str
    explanation_a: str
    explanation_b: str
    explanation_c: str
    explanation_d: str
    explanation_e: str
    correct_answer: str
    created_at: datetime
    support_materials: list[QuestionSupportMaterialResponse]
