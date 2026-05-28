import base64
from typing import Any

from openai import OpenAI

from src.configs.configs import settings
from src.models.models import QuestionAssets
from src.utils.s3_storage import S3Storage

client = OpenAI()

SUPPORTED_ASSET_TYPES = {
    "text",
    "table",
    "chart",
    "image",
    "map",
    "diagram",
    "infographic",
}
SUPPORTED_RENDERING_MODES = {"inline_text", "structured_data", "generated_image"}
SUPPORTED_POSITIONS = {"before_statement", "after_statement"}
VISUAL_ASSET_TYPES = {"image", "map", "infographic"}
STRUCTURED_ASSET_TYPES = {"table", "chart", "diagram"}


def validate_support_materials(materials: Any) -> str | None:
    if not isinstance(materials, list) or not materials:
        return "AI response must include at least one support material."

    if len(materials) > 2:
        return "AI response returned more than two support materials."

    for index, raw_material in enumerate(materials, start=1):
        if not isinstance(raw_material, dict):
            return f"Support material #{index} is not an object."

        asset_type = raw_material.get("asset_type")
        rendering_mode = raw_material.get("rendering_mode")
        position = raw_material.get("position")

        if asset_type not in SUPPORTED_ASSET_TYPES:
            return f"Support material #{index} has an invalid asset_type."
        if rendering_mode not in SUPPORTED_RENDERING_MODES:
            return f"Support material #{index} has an invalid rendering_mode."
        if position not in SUPPORTED_POSITIONS:
            return f"Support material #{index} has an invalid position."

        if asset_type == "text":
            if rendering_mode != "inline_text":
                return (
                    f"Support material #{index} with asset_type text must use "
                    "rendering_mode inline_text."
                )
            if not str(raw_material.get("content", "")).strip():
                return f"Support material #{index} is missing content."
            continue

        if asset_type in STRUCTURED_ASSET_TYPES:
            if rendering_mode != "structured_data":
                return (
                    f"Support material #{index} with asset_type {asset_type} must use "
                    "rendering_mode structured_data."
                )
            if not isinstance(raw_material.get("data"), dict) or not raw_material.get(
                "data"
            ):
                return f"Support material #{index} is missing structured data."
            if asset_type == "diagram":
                diagram_type = str(raw_material["data"].get("diagram_type", "")).strip()
                if not diagram_type:
                    return (
                        f"Support material #{index} with asset_type diagram is missing "
                        "diagram_type."
                    )
            continue

        if asset_type in VISUAL_ASSET_TYPES:
            if rendering_mode != "generated_image":
                return (
                    f"Support material #{index} with asset_type {asset_type} must use "
                    "rendering_mode generated_image."
                )
            if not str(raw_material.get("image_generation_prompt", "")).strip():
                return (
                    f"Support material #{index} is missing image_generation_prompt."
                )
            if not str(raw_material.get("alt_text", "")).strip():
                return f"Support material #{index} is missing alt_text."
            continue

    return None


def normalize_support_materials(materials: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_materials = []

    for index, raw_material in enumerate(materials):
        asset_type = raw_material["asset_type"].strip().lower()
        rendering_mode = raw_material["rendering_mode"].strip().lower()
        position = raw_material["position"].strip().lower()
        title = _clean_optional_text(raw_material.get("title"))
        caption = _clean_optional_text(raw_material.get("caption"))
        alt_text = _clean_optional_text(raw_material.get("alt_text"))
        source_label = _clean_optional_text(raw_material.get("source_label"))
        content = _clean_optional_text(raw_material.get("content"))
        metadata = raw_material.get("data")

        if not isinstance(metadata, dict):
            metadata = {}

        if raw_material.get("image_generation_prompt"):
            metadata["image_generation_prompt"] = raw_material[
                "image_generation_prompt"
            ].strip()

        normalized_materials.append(
            {
                "asset_type": asset_type,
                "rendering_mode": rendering_mode,
                "position": position,
                "display_order": index,
                "title": title,
                "caption": caption,
                "alt_text": alt_text,
                "source_label": source_label,
                "content": content,
                "data": metadata or None,
            }
        )

    return normalized_materials


def build_question_assets(
    question_id,
    support_materials: list[dict[str, Any]],
) -> list[QuestionAssets]:
    assets: list[QuestionAssets] = []

    for material in support_materials:
        asset = QuestionAssets(
            question_id=question_id,
            asset_type=material["asset_type"],
            rendering_mode=material["rendering_mode"],
            position=material["position"],
            display_order=material["display_order"],
            title=material["title"],
            caption=material["caption"],
            alt_text=material["alt_text"],
            source_label=material["source_label"],
            content=material["content"],
            asset_metadata=material["data"],
            storage_status="not_required",
        )

        if (
            material["asset_type"] in VISUAL_ASSET_TYPES
            and material["rendering_mode"] == "generated_image"
        ):
            _attach_visual_asset_storage(asset, question_id)

        assets.append(asset)

    return assets


def serialize_support_material(asset: QuestionAssets) -> dict[str, Any]:
    return {
        "id": asset.id,
        "asset_type": asset.asset_type,
        "rendering_mode": asset.rendering_mode,
        "position": asset.position,
        "display_order": asset.display_order,
        "storage_status": asset.storage_status,
        "title": asset.title,
        "caption": asset.caption,
        "alt_text": asset.alt_text,
        "source_label": asset.source_label,
        "content": asset.content,
        "storage_provider": asset.storage_provider,
        "storage_key": asset.storage_key,
        "public_url": asset.public_url,
        "mime_type": asset.mime_type,
        "data": asset.asset_metadata,
    }


def _attach_visual_asset_storage(asset: QuestionAssets, question_id) -> None:
    image_generation_prompt = None
    if isinstance(asset.asset_metadata, dict):
        image_generation_prompt = asset.asset_metadata.get("image_generation_prompt")

    if not image_generation_prompt or not settings.QUESTION_ASSETS_ENABLE_IMAGE_GENERATION:
        asset.storage_status = "pending_storage_configuration"
        return

    if not S3Storage.is_enabled():
        asset.storage_provider = "s3"
        asset.storage_status = "pending_storage_configuration"
        return

    try:
        image_bytes, mime_type, extension = _generate_image_bytes(
            prompt=image_generation_prompt,
        )
        upload_result = S3Storage.upload_question_asset(
            question_id=question_id,
            extension=extension,
            body=image_bytes,
            content_type=mime_type,
        )
        asset.storage_provider = upload_result["storage_provider"]
        asset.storage_key = upload_result["storage_key"]
        asset.public_url = upload_result["public_url"]
        asset.mime_type = mime_type
        asset.storage_status = "stored"
    except Exception as exc:
        asset.storage_provider = "s3"
        asset.storage_status = "generation_failed"
        asset.asset_metadata = {
            **(asset.asset_metadata or {}),
            "storage_error": str(exc),
        }


def _generate_image_bytes(*, prompt: str) -> tuple[bytes, str, str]:
    try:
        response = client.images.generate(
            model=settings.OPENAI_IMAGE_MODEL,
            prompt=prompt,
            size=settings.OPENAI_IMAGE_SIZE,
            quality=settings.OPENAI_IMAGE_QUALITY,
        )
    except TypeError:
        response = client.images.generate(
            model=settings.OPENAI_IMAGE_MODEL,
            prompt=prompt,
            size=settings.OPENAI_IMAGE_SIZE,
        )

    image_base64 = getattr(response.data[0], "b64_json", None)
    if not image_base64:
        raise ValueError("Image generation did not return base64 data.")

    extension = settings.OPENAI_IMAGE_OUTPUT_FORMAT.lower()
    mime_type = f"image/{extension}"
    return base64.b64decode(image_base64), mime_type, extension


def _clean_optional_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None
