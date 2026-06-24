import uuid
from typing import Optional
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.services.question_asset_service import (
    normalize_question_assets,
    prepare_question_asset_record,
)


class CreateQuestionAssetRouteRequest(BaseModel):
    asset_type: str
    rendering_mode: str
    position: str
    display_order: int = 0
    storage_status: str | None = None
    title: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    source_label: str | None = None
    content: str | None = None
    public_url: str | None = None
    mime_type: str | None = None
    data: dict[str, Any] | None = None
    image_generation_prompt: str | None = None
    file_base64: str | None = None

    model_config = ConfigDict(
        extra="ignore",
        json_schema_extra={
            "example": {
                "asset_type": "table",
                "rendering_mode": "structured_data",
                "position": "before_statement",
                "display_order": 0,
                "title": "Tabela de apoio",
                "caption": "Dados usados na resolucao",
                "data": {
                    "columns": ["Aluno", "Pontos"],
                    "rows": [["Ana", "14"], ["Bruno", "16"]],
                },
            }
        },
    )

    @model_validator(mode="after")
    def validate_shape(self):
        normalize_question_assets([BaseModel.model_dump(self)])
        return self

    def model_dump(self, *args, **kwargs):
        raw_payload = super().model_dump(*args, **kwargs)
        normalized_asset = normalize_question_assets([raw_payload])[0]
        return prepare_question_asset_record(
            normalized_asset,
            storage_owner_id=uuid.uuid4(),
        )


class QuestionAssetRouteResponse(BaseModel):
    id: Optional[UUID] = None
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
    data: dict[str, Any] | None = Field(
        default=None,
        validation_alias="metadata_",
    )
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "12345678-1234-1234-1234-123456789012",
                "asset_type": "table",
                "rendering_mode": "structured_data",
                "position": "before_statement",
                "display_order": 0,
                "storage_status": "not_required",
                "title": "Tabela 1",
                "caption": "Dados usados na resolucao da questao",
                "source_label": "Texto elaborado para fins educacionais.",
                "content": None,
                "storage_provider": None,
                "storage_key": None,
                "public_url": None,
                "mime_type": None,
                "data": {
                    "columns": ["Aluno", "Pontos"],
                    "rows": [["Ana", "14"], ["Bruno", "16"]],
                },
                "created_at": "2026-06-18T10:00:00",
            }
        },
    )
