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
        question_id: uuid.UUID,
        extension: str,
        body: bytes,
        content_type: str,
    ) -> dict[str, str]:
        if not S3Storage.is_enabled():
            raise S3StorageError("S3 is not fully configured.")

        key_prefix = settings.S3_KEY_PREFIX.strip("/")
        object_key = (
            f"{key_prefix}/{question_id}/{uuid.uuid4()}.{extension.lstrip('.')}"
            if key_prefix
            else f"{question_id}/{uuid.uuid4()}.{extension.lstrip('.')}"
        )

        client = boto3.client(
            "s3",
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
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

        if settings.S3_PUBLIC_BASE_URL:
            return f"{settings.S3_PUBLIC_BASE_URL.rstrip('/')}/{encoded_key}"

        if settings.S3_ENDPOINT_URL:
            return (
                f"{settings.S3_ENDPOINT_URL.rstrip('/')}/"
                f"{settings.S3_BUCKET}/{encoded_key}"
            )

        if settings.S3_REGION:
            return (
                f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com/"
                f"{encoded_key}"
            )

        return f"https://{settings.S3_BUCKET}.s3.amazonaws.com/{encoded_key}"
