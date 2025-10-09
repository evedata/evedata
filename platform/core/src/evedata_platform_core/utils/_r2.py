import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import boto3
from botocore.exceptions import ClientError

if TYPE_CHECKING:
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


def r2_key_exists(bucket: str, key: str, *, r2: "R2Client") -> bool:
    """Check if a file exists in R2."""
    try:
        r2.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if "Error" in e.response and e.response["Error"].get("Code") == "404":
            return False
        raise
    else:
        return True


def r2_list_keys(bucket: str, prefix: str, *, r2: "R2Client") -> list[str]:
    """List files in an R2 bucket with the given prefix."""
    paginator = r2.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    keys: list[str] = []
    for page in page_iterator:
        contents = page.get("Contents", [])
        keys.extend([o["Key"] for o in contents if "Key" in o])
    return sorted(keys)


def r2_get_json_object(bucket: str, key: str, *, r2: "R2Client") -> dict[str, Any]:
    """Read a JSON object from R2."""
    obj = r2.get_object(Bucket=bucket, Key=key)
    return json.loads(obj["Body"].read())


def r2_rename_prefix(
    bucket: str, old_prefix: str, new_prefix: str, *, r2: "R2Client"
) -> None:
    """Rename all files in an R2 bucket with the given prefix."""
    keys = r2_list_keys(bucket, old_prefix, r2=r2)
    for key in keys:
        new_key = key.replace(old_prefix, new_prefix, 1)
        r2.copy_object(
            Bucket=bucket,
            CopySource={"Bucket": bucket, "Key": key},
            Key=new_key,
        )
        r2.delete_object(Bucket=bucket, Key=key)


def r2_download(bucket: str, key: str, download_path: Path, r2: "R2Client") -> None:
    """Download a file from R2."""
    if download_path.is_dir():
        download_path = download_path / key.split("/")[-1]
    r2.download_file(bucket, key, str(download_path))


def r2_upload(
    bucket: str,
    key: str,
    source: "dict[str, Any] | str | Path",
    *,
    r2: "R2Client",
) -> None:
    """Upload a JSON object, string, or file to R2."""
    if isinstance(source, dict):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(source, tmp)
            tmp_path = tmp.name
        try:
            r2.upload_file(tmp_path, bucket, key)
        finally:
            Path(tmp_path).unlink()
    elif isinstance(source, str):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp.write(source)
            tmp_path = tmp.name
        try:
            r2.upload_file(tmp_path, bucket, key)
        finally:
            Path(tmp_path).unlink()
    else:
        r2.upload_file(str(source), bucket, key)


def r2_upload_dir(
    bucket: str,
    prefix: str,
    source: "Path",
    *,
    r2: "R2Client",
) -> None:
    """Upload a JSON object, string, or file to R2."""
    if not source.is_dir():
        msg = "Source must be a directory"
        raise ValueError(msg)

    for source_path in Path.glob(source, "**/*"):
        if source_path.is_dir():
            continue
        key = "/".join([prefix, str(source_path.relative_to(source))])
        r2.upload_file(str(source_path), bucket, key)
