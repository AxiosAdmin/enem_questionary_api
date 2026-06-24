from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.schemas.ai_question_schema import GeneratedQuestionResponse


class ManualQuestionAssetRequest(BaseModel):
    asset_type: Literal[
        "text",
        "table",
        "chart",
        "image",
        "map",
        "diagram",
        "infographic",
    ]
    rendering_mode: Literal["inline_text", "structured_data", "generated_image"]
    position: Literal["before_statement", "after_statement"]
    title: str | None = None
    caption: str | None = None
    alt_text: str | None = None
    source_label: str | None = None
    content: str | None = None
    data: dict[str, Any] | None = None
    image_generation_prompt: str | None = None
    public_url: str | None = None
    mime_type: str | None = None
    file_base64: str | None = None

    @model_validator(mode="after")
    def validate_material_shape(self):
        if self.asset_type == "text":
            if self.rendering_mode != "inline_text":
                raise ValueError(
                    "Materials with asset_type text must use rendering_mode inline_text."
                )
            if not (self.content or "").strip():
                raise ValueError("Text materials must include content.")
            return self

        if self.asset_type in {"table", "chart", "diagram"}:
            if self.rendering_mode != "structured_data":
                raise ValueError(
                    "Structured materials must use rendering_mode structured_data."
                )
            if not isinstance(self.data, dict) or not self.data:
                raise ValueError("Structured materials must include data.")
            if (
                self.asset_type == "diagram"
                and not str(self.data.get("diagram_type", "")).strip()
            ):
                raise ValueError("Diagram materials must include data.diagram_type.")
            return self

        if self.rendering_mode != "generated_image":
            raise ValueError(
                "Visual materials must use rendering_mode generated_image."
            )
        if not (self.alt_text or "").strip():
            raise ValueError("Visual materials must include alt_text.")

        image_sources = sum(
            bool(value and str(value).strip())
            for value in (
                self.image_generation_prompt,
                self.public_url,
                self.file_base64,
            )
        )
        if image_sources != 1:
            raise ValueError(
                "Visual materials must include exactly one source: "
                "image_generation_prompt, public_url or file_base64."
            )
        return self


class CreateQuestionRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=100)
    subtopic: str = Field(min_length=1)
    subtopic_description: str = Field(min_length=1)
    diversity_mode: str = Field(min_length=1)
    question: str = Field(min_length=1)
    answer_a: str = Field(min_length=1)
    answer_b: str = Field(min_length=1)
    answer_c: str = Field(min_length=1)
    answer_d: str = Field(min_length=1)
    answer_e: str = Field(min_length=1)
    explanation_a: str = Field(min_length=1)
    explanation_b: str = Field(min_length=1)
    explanation_c: str = Field(min_length=1)
    explanation_d: str = Field(min_length=1)
    explanation_e: str = Field(min_length=1)
    correct_answer: Literal["A", "B", "C", "D", "E"]
    question_assets: list[ManualQuestionAssetRequest] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "Matematica",
                "subtopic": "Estatistica",
                "subtopic_description": "Leitura de tabela e media aritmetica",
                "diversity_mode": "manual",
                "question": "A tabela apresenta a pontuacao de cinco estudantes...",
                "answer_a": "12",
                "answer_b": "14",
                "answer_c": "16",
                "answer_d": "18",
                "answer_e": "20",
                "explanation_a": "Somando os valores e dividindo por cinco...",
                "explanation_b": "Resposta incorreta...",
                "explanation_c": "Resposta incorreta...",
                "explanation_d": "Resposta incorreta...",
                "explanation_e": "Resposta incorreta...",
                "correct_answer": "C",
                "question_assets": [
                    {
                        "asset_type": "table",
                        "rendering_mode": "structured_data",
                        "position": "before_statement",
                        "title": "Tabela 1",
                        "caption": "Pontuacao obtida pelos estudantes",
                        "data": {
                            "columns": ["Estudante", "Pontos"],
                            "rows": [
                                ["Ana", "14"],
                                ["Bruno", "16"],
                                ["Clara", "12"],
                            ],
                        },
                    }
                ],
            }
        }
    )


class CreateQuestionResponse(GeneratedQuestionResponse):
    pass
