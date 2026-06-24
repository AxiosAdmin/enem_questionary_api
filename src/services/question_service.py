from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import QuestionAssetQuestions, QuestionAssets, Questions
from src.schemas.question_schema import CreateQuestionRequest
from src.services.question_asset_service import (
    build_question_assets,
    normalize_question_assets,
    serialize_question_asset,
)


class QuestionService:
    @staticmethod
    async def create_question(
        request: CreateQuestionRequest,
        db: AsyncSession,
    ) -> dict[str, Any]:
        payload = request.model_dump()
        question_assets = normalize_question_assets(payload["question_assets"])

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

        return await QuestionService.persist_question(
            question=question,
            question_assets=question_assets,
            db=db,
        )

    @staticmethod
    async def persist_question(
        *,
        question: Questions,
        question_assets: list[dict[str, Any]],
        db: AsyncSession,
    ) -> dict[str, Any]:
        db.add(question)
        await db.flush()

        assets = build_question_assets(question.id, question_assets)
        for asset in assets:
            db.add(asset)

        await db.flush()
        for asset in assets:
            db.add(
                QuestionAssetQuestions(
                    question_id=question.id,
                    question_asset_id=asset.id,
                )
            )
        await db.flush()
        await db.commit()
        await db.refresh(question)

        return QuestionService.serialize_question(question, assets)

    @staticmethod
    async def persist_question_with_existing_assets(
        *,
        question: Questions,
        existing_assets: list[QuestionAssets],
        db: AsyncSession,
    ) -> dict[str, Any]:
        db.add(question)
        await db.flush()

        for asset in existing_assets:
            db.add(
                QuestionAssetQuestions(
                    question_id=question.id,
                    question_asset_id=asset.id,
                )
            )
        await db.flush()
        await db.commit()
        await db.refresh(question)

        return QuestionService.serialize_question(question, existing_assets)

    @staticmethod
    def serialize_question(question: Questions, assets: list) -> dict[str, Any]:
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
            "question_assets": [
                serialize_question_asset(asset)
                for asset in sorted(assets, key=lambda item: item.display_order)
            ],
        }
