import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from aws_vibe_guru.aws_sqs import read_aws_credentials


def create_s3_connection(access_key=None, secret_key=None, region=None):
    if not all([access_key, secret_key, region]):
        credentials = read_aws_credentials()
        access_key = access_key or credentials["access_key"]
        secret_key = secret_key or credentials["secret_key"]
        region = region or credentials["region"]

    try:
        return boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
    except NoCredentialsError as e:
        raise ValueError("Invalid AWS credentials provided") from e
    except ClientError as e:
        raise ValueError(f"Failed to connect to AWS S3: {e}") from e


def list_buckets():
    try:
        s3_client = create_s3_connection()
        response = s3_client.list_buckets()

        buckets = []
        for bucket in response.get("Buckets", []):
            buckets.append(
                {"name": bucket["Name"], "creation_date": bucket["CreationDate"].strftime("%Y-%m-%d %H:%M:%S UTC")}
            )

        return buckets

    except ClientError as e:
        raise ValueError(f"Failed to list S3 buckets: {e}") from e


def list_bucket_objects(bucket_name, prefix=None, max_keys=1000):
    try:
        s3_client = create_s3_connection()

        kwargs = {"Bucket": bucket_name, "MaxKeys": max_keys}

        if prefix:
            kwargs["Prefix"] = prefix

        objects = []
        continuation_token = None

        while True:
            if continuation_token:
                kwargs["ContinuationToken"] = continuation_token

            response = s3_client.list_objects_v2(**kwargs)

            for obj in response.get("Contents", []):
                size_mb = obj["Size"] / (1024 * 1024)
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "size_mb": f"{size_mb:.2f}",
                        "last_modified": obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S UTC"),
                        "storage_class": obj.get("StorageClass", "STANDARD"),
                    }
                )

            if not response.get("IsTruncated"):
                break

            continuation_token = response.get("NextContinuationToken")

            if len(objects) >= max_keys:
                break

        return {
            "bucket_name": bucket_name,
            "prefix": prefix or "all",
            "total_objects": len(objects),
            "objects": objects,
        }

    except ClientError as e:
        raise ValueError(f"Failed to list objects in bucket '{bucket_name}': {e}") from e


def get_object_info(bucket_name, object_key):
    try:
        s3_client = create_s3_connection()

        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        size_mb = response["ContentLength"] / (1024 * 1024)

        object_info = {
            "bucket": bucket_name,
            "key": object_key,
            "size": response["ContentLength"],
            "size_mb": f"{size_mb:.2f}",
            "last_modified": response["LastModified"].strftime("%Y-%m-%d %H:%M:%S UTC"),
            "content_type": response.get("ContentType", "N/A"),
            "etag": response.get("ETag", "N/A").strip('"'),
            "storage_class": response.get("StorageClass", "STANDARD"),
            "metadata": response.get("Metadata", {}),
            "version_id": response.get("VersionId", "N/A"),
        }

        return object_info

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise ValueError(f"Object '{object_key}' not found in bucket '{bucket_name}'") from e
        raise ValueError(f"Failed to get object info: {e}") from e


def read_object_content(bucket_name, object_key, encoding="utf-8"):
    try:
        s3_client = create_s3_connection()

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

        content_bytes = response["Body"].read()

        try:
            content = content_bytes.decode(encoding)
            is_binary = False
        except UnicodeDecodeError:
            content = None
            is_binary = True

        result = {
            "bucket": bucket_name,
            "key": object_key,
            "size": len(content_bytes),
            "content_type": response.get("ContentType", "N/A"),
            "is_binary": is_binary,
            "encoding": encoding if not is_binary else None,
            "content": content,
        }

        return result

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            raise ValueError(f"Object '{object_key}' not found in bucket '{bucket_name}'") from e
        raise ValueError(f"Failed to read object content: {e}") from e
