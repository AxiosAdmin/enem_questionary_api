import json

from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.enem_question_common import validate_generated_question_payload
from src.models.models import Questions
from src.services.question_asset_service import (
    build_question_assets,
    normalize_support_materials,
    serialize_support_material,
)
from src.configs.configs import settings

client = OpenAI()


async def generate_enem_question(
    topic: str,
    build_context_fn,
    build_prompt_fn,
    db: AsyncSession,
    *,
    max_attempts: int = 4,
) -> dict:
    last_error = None
    selected_context = build_context_fn(topic)

    for _ in range(max_attempts):
        response = client.responses.create(
            model=settings.OPENAI_TEXT_MODEL,
            input=build_prompt_fn(**selected_context),
        )
        response_text = response.output[0].content[0].text

        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError:
            last_error = ValueError("AI response is not a valid JSON object.")
            continue

        validation_error = validate_generated_question_payload(payload)
        if validation_error is not None:
            last_error = ValueError(validation_error)
            continue

        payload.update(selected_context)
        support_materials = normalize_support_materials(payload["support_materials"])
        question = Questions(
            topic=payload["topic"],
            subtopic=payload["subtopic"],
            subtopic_description=payload["subtopic_description"],
            diversity_mode=payload["diversity_mode"],
            question=payload["question"],
            answer_a=payload["answer_a"],
            answer_b=payload["answer_b"],
            answer_c=payload["answer_c"],
            answer_d=payload["answer_d"],
            answer_e=payload["answer_e"],
            explanation_a=payload["explanation_a"],
            explanation_b=payload["explanation_b"],
            explanation_c=payload["explanation_c"],
            explanation_d=payload["explanation_d"],
            explanation_e=payload["explanation_e"],
            correct_answer=payload["correct_answer"],
        )
        db.add(question)
        await db.flush()

        assets = build_question_assets(question.id, support_materials)
        for asset in assets:
            db.add(asset)

        await db.flush()
        await db.commit()
        await db.refresh(question)
        return _serialize_generated_question(question, assets)

    raise last_error or ValueError("Unable to generate a valid ENEM question.")


def _serialize_generated_question(question: Questions, assets: list) -> dict:
    return {
        "id": question.id,
        "topic": question.topic,
        "subtopic": question.subtopic,
        "subtopic_description": question.subtopic_description,
        "diversity_mode": question.diversity_mode,
        "question": question.question,
        "answer_a": question.answer_a,
        "answer_b": question.answer_b,
        "answer_c": question.answer_c,
        "answer_d": question.answer_d,
        "answer_e": question.answer_e,
        "explanation_a": question.explanation_a,
        "explanation_b": question.explanation_b,
        "explanation_c": question.explanation_c,
        "explanation_d": question.explanation_d,
        "explanation_e": question.explanation_e,
        "correct_answer": question.correct_answer,
        "created_at": question.created_at,
        "support_materials": [
            serialize_support_material(asset)
            for asset in sorted(assets, key=lambda item: item.display_order)
        ],
    }
