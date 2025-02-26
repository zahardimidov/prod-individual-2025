from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from infra.config import settings
from types_aiobotocore_s3.client import S3Client


@asynccontextmanager
async def get_client(bucket_name) -> AsyncGenerator['S3Client', None]:
    session = get_session()
    config = dict(
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        endpoint_url=settings.MINIO_URL,
    )

    async with session.create_client("s3", **config) as client:
        client: S3Client
        try:
            await client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                await client.create_bucket(Bucket=bucket_name)
            raise

        yield client
