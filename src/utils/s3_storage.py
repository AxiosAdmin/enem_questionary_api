from urllib.parse import quote
import uuid

import boto3

from src.configs.configs import settings


class S3StorageError(RuntimeError):
    pass


class S3Storage:
    @staticmethod
    def is_enabled() -> bool:
        return bool(
            settings.S3_ENABLED
            and settings.S3_BUCKET
            and settings.S3_ACCESS_KEY_ID
            and settings.S3_SECRET_ACCESS_KEY
        )

    @staticmethod
    def upload_question_asset(
        *,
        owner_id: uuid.UUID,
        extension: str,
        body: bytes,
        content_type: str,
    ) -> dict[str, str]:
        return S3Storage._upload_asset(
            object_owner_prefix=str(owner_id),
            extension=extension,
            body=body,
            content_type=content_type,
        )

    @staticmethod
    def _upload_asset(
        *,
        object_owner_prefix: str,
        extension: str,
        body: bytes,
        content_type: str,
    ) -> dict[str, str]:
        if not S3Storage.is_enabled():
            raise S3StorageError("S3 is not fully configured.")

        key_prefix = settings.S3_KEY_PREFIX.strip("/")
        object_key = (
            f"{key_prefix}/{object_owner_prefix}/{uuid.uuid4()}.{extension.lstrip('.')}"
            if key_prefix
            else f"{object_owner_prefix}/{uuid.uuid4()}.{extension.lstrip('.')}"
        )

        client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
            endpoint_url=_normalize_optional_setting(settings.S3_ENDPOINT_URL),
        )
        client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=object_key,
            Body=body,
            ContentType=content_type,
        )

        return {
            "storage_provider": "s3",
            "storage_key": object_key,
            "public_url": S3Storage.build_public_url(object_key),
        }

    @staticmethod
    def build_public_url(object_key: str) -> str:
        encoded_key = quote(object_key)

        public_base_url = _normalize_optional_setting(settings.S3_PUBLIC_BASE_URL)
        endpoint_url = _normalize_optional_setting(settings.S3_ENDPOINT_URL)

        if public_base_url:
            return f"{public_base_url.rstrip('/')}/{encoded_key}"

        if endpoint_url:
            return f"{endpoint_url.rstrip('/')}/" f"{settings.S3_BUCKET}/{encoded_key}"

        if settings.S3_REGION:
            return (
                f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com/"
                f"{encoded_key}"
            )

        return f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{encoded_key}"


def _normalize_optional_setting(value: str | None) -> str | None:
    if value is None:
        return None

    normalized_value = value.strip()
    return normalized_value or None
