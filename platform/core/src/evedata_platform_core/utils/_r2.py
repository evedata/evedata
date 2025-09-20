from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from pathlib import Path

    from types_boto3_s3 import S3Client as R2Client

    from evedata_platform_core import Configuration


def r2_client_from_config(config: "Configuration") -> "R2Client":
    """Create an R2 client from the platform configuration."""
    return boto3.client(  # pyright: ignore[reportUnknownMemberType]
        "s3",
        endpoint_url=config.r2_endpoint_url,
        aws_access_key_id=config.r2_access_key_id,
        aws_secret_access_key=config.r2_secret_access_key,
        region_name=config.r2_region,
    )


def r2_download(
    client: "R2Client", bucket: str, key: str, file_path: "str | Path"
) -> None:
    """Download a file from R2."""
    client.download_file(bucket, key, str(file_path))


def r2_exists(client: "R2Client", bucket: str, key: str) -> bool:
    """Check if a file exists in R2."""
    try:
        client.head_object(Bucket=bucket, Key=key)
    except client.exceptions.NoSuchKey:
        return False
    else:
        return True


def r2_list_keys(client: "R2Client", bucket: str, prefix: str) -> list[str]:
    """List files in an R2 bucket with the given prefix."""
    paginator = client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    keys: list[str] = []
    for page in page_iterator:
        contents = page.get("Contents", [])
        keys.extend([o["Key"] for o in contents if "Key" in o])
    return sorted(keys)


def r2_rename_prefix(
    client: "R2Client", bucket: str, old_prefix: str, new_prefix: str
) -> None:
    """Rename all files in an R2 bucket with the given prefix."""
    keys = r2_list_keys(client, bucket, old_prefix)
    for key in keys:
        new_key = key.replace(old_prefix, new_prefix, 1)
        client.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": key},
            Key=new_key,
        )
        client.delete_object(Bucket=bucket, Key=key)


def r2_upload(
    client: "R2Client", bucket: str, key: str, file_path: "str | Path"
) -> None:
    """Upload a file to R2."""
    client.upload_file(str(file_path), bucket, key)
