import configparser
import datetime
import os.path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

ONE_DAY_IN_SECONDS = 86400
ONE_HOUR_IN_SECONDS = 3600


def read_aws_credentials():
    """Read AWS credentials from ~/.aws/credentials file or environment variables.

    Returns:
        dict: Dictionary containing access_key, secret_key, and region

    """
    credentials_file = os.path.expanduser("~/.aws/credentials")
    if os.path.exists(credentials_file):
        config = configparser.ConfigParser()
        config.read(credentials_file)

        if "default" in config.sections():
            return {
                "access_key": config.get("default", "aws_access_key_id", fallback=""),
                "secret_key": config.get("default", "aws_secret_access_key", fallback=""),
                "region": config.get("default", "region", fallback="us-east-1"),
            }

    credentials = {
        "access_key": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }

    return credentials


def create_sqs_connection(access_key=None, secret_key=None, region=None):
    """Establish connection with AWS SQS service.

    Args:
        access_key: AWS access key ID (optional, will read from credentials if not provided)
        secret_key: AWS secret access key (optional, will read from credentials if not provided)
        region: AWS region (optional, will read from credentials if not provided)

    Returns:
        boto3.client: SQS client object

    Raises:
        ValueError: When credentials are invalid or missing or AWS connection fails
    """
    if not all([access_key, secret_key, region]):
        credentials = read_aws_credentials()
        access_key = access_key or credentials["access_key"]
        secret_key = secret_key or credentials["secret_key"]
        region = region or credentials["region"]

    try:
        return boto3.client(
            "sqs",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
    except NoCredentialsError as e:
        raise ValueError("Invalid AWS credentials provided") from e
    except ClientError as e:
        raise ValueError(f"Failed to connect to AWS SQS: {e}") from e


def list_sqs_queues(sqs_client, queue_name_prefix=None, max_results=1000):
    """List all SQS queues with optional filtering.

    Args:
        sqs_client: boto3 SQS client object
        queue_name_prefix: Optional prefix to filter queue names
        max_results: Maximum number of queues to return (default 1000)

    Returns:
        list: List of dictionaries containing queue information with keys:
              'name', 'url'

    Raises:
        ValueError: When AWS API call fails
    """
    try:
        kwargs = {"MaxResults": min(max_results, 1000)}
        if queue_name_prefix:
            kwargs["QueueNamePrefix"] = queue_name_prefix

        response = sqs_client.list_queues(**kwargs)
        queue_urls = response.get("QueueUrls", [])

        queues = []
        for url in queue_urls:
            queue_name = url.split("/")[-1]
            queues.append({"name": queue_name, "url": url})

        return queues

    except ClientError as e:
        raise ValueError(f"Failed to list SQS queues: {e}") from e


def get_queue_oldest_message(sqs_client, queue_url, days=7):
    """Get approximate age of oldest message in the queue over time.

    Args:
        sqs_client: boto3 SQS client object
        queue_url: The URL of the queue to get metrics for
        days: Number of days to look back (default: 7)

    Returns:
        dict: Dictionary containing age metrics with values in seconds

    Raises:
        ValueError: When AWS API call fails
    """
    try:
        cloudwatch = boto3.client("cloudwatch")

        queue_name = queue_url.split("/")[-1]

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/SQS",
            MetricName="ApproximateAgeOfOldestMessage",
            Dimensions=[{"Name": "QueueName", "Value": queue_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=days),
            EndTime=datetime.datetime.utcnow(),
            Period=ONE_HOUR_IN_SECONDS,
            Statistics=["Maximum"],
        )

        datapoints = response.get("Datapoints", [])
        datapoints.sort(key=lambda x: x["Timestamp"])

        def format_age(seconds):
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            minutes = (seconds % 3600) // 60
            if days > 0:
                return f"{int(days)}d {int(hours)}h {int(minutes)}m"
            elif hours > 0:
                return f"{int(hours)}h {int(minutes)}m"
            else:
                return f"{int(minutes)}m"

        metrics = {
            "queue_name": queue_name,
            "metric": "ApproximateAgeOfOldestMessage",
            "period": f"last_{days}_days",
            "current_max_age": format_age(datapoints[-1]["Maximum"]) if datapoints else "0m",
            "period_max_age": format_age(max((p["Maximum"] for p in datapoints), default=0)),
            "hourly_data": [
                {"timestamp": point["Timestamp"].strftime("%Y-%m-%d %H:%M UTC"), "age": format_age(point["Maximum"])}
                for point in datapoints
            ],
        }

        return metrics

    except ClientError as e:
        raise ValueError(f"Failed to get queue age metrics: {e}") from e


def analyze_queue_volume(queue_url, days=15):
    """Analyze message volume trends for a queue.

    Args:
        sqs_client: boto3 SQS client object
        queue_url: The URL of the queue to analyze
        days: Number of days to look back (default: 15)

    Returns:
        dict: Dictionary containing volume analysis with keys:
            'daily_data': List of daily volumes
            'max_volume_day': Day with highest volume
            'max_volume': Highest daily volume
            'second_max_day': Day with second highest volume
            'second_max_volume': Second highest daily volume
            'volume_difference': Difference between max and second max
            'volume_increase_percent': Percentage increase from second to max

    Raises:
        ValueError: When AWS API call fails
    """
    try:
        cloudwatch = boto3.client("cloudwatch")
        queue_name = queue_url.split("/")[-1]

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/SQS",
            MetricName="NumberOfMessagesReceived",
            Dimensions=[{"Name": "QueueName", "Value": queue_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=days),
            EndTime=datetime.datetime.utcnow(),
            Period=ONE_DAY_IN_SECONDS,
            Statistics=["Sum"],
        )

        datapoints = response.get("Datapoints", [])
        datapoints.sort(key=lambda x: x["Timestamp"])

        daily_data = [
            {"date": point["Timestamp"].strftime("%Y-%m-%d"), "value": int(point["Sum"])} for point in datapoints
        ]

        if len(daily_data) < 2:
            return {
                "daily_data": daily_data,
                "max_volume_day": daily_data[0]["date"] if daily_data else None,
                "max_volume": daily_data[0]["value"] if daily_data else 0,
                "second_max_day": None,
                "second_max_volume": 0,
                "volume_difference": daily_data[0]["value"] if daily_data else 0,
                "volume_increase_percent": 100 if daily_data else 0,
            }

        volume_sorted = sorted(daily_data, key=lambda x: x["value"], reverse=True)
        max_day = volume_sorted[0]
        second_max_day = volume_sorted[1]

        volume_diff = max_day["value"] - second_max_day["value"]
        volume_percent = (volume_diff / second_max_day["value"] * 100) if second_max_day["value"] > 0 else 100

        all_volumes = [day["value"] for day in daily_data]
        mean_volume = sum(all_volumes) / len(all_volumes)

        sorted_volumes = sorted(all_volumes)
        mid = len(sorted_volumes) // 2
        median_volume = sorted_volumes[mid]
        if len(sorted_volumes) % 2 == 0:
            median_volume = (sorted_volumes[mid - 1] + sorted_volumes[mid]) / 2

        mean_diff = max_day["value"] - mean_volume
        mean_percent = (mean_diff / mean_volume * 100) if mean_volume > 0 else 100

        median_diff = max_day["value"] - median_volume
        median_percent = (median_diff / median_volume * 100) if median_volume > 0 else 100

        return {
            "daily_data": daily_data,
            "max_volume_day": max_day["date"],
            "max_volume": max_day["value"],
            "second_max_day": second_max_day["date"],
            "second_max_volume": second_max_day["value"],
            "volume_difference": volume_diff,
            "volume_increase_percent": volume_percent,
            "mean_volume": mean_volume,
            "mean_difference": mean_diff,
            "mean_increase_percent": mean_percent,
            "median_volume": median_volume,
            "median_difference": median_diff,
            "median_increase_percent": median_percent,
        }

    except ClientError as e:
        raise ValueError(f"Failed to analyze queue volume: {e}") from e


def get_queue_metrics(queue_url, days=7):
    """Get CloudWatch metrics for a specific queue.

    Args:
        sqs_client: boto3 SQS client object
        queue_url: The URL of the queue to get metrics for
        days: Number of days to look back (default: 7)

    Returns:
        dict: Dictionary containing queue metrics with values

    Raises:
        ValueError: When AWS API call fails
    """
    try:
        cloudwatch = boto3.client("cloudwatch")

        queue_name = queue_url.split("/")[-1]

        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/SQS",
            MetricName="NumberOfMessagesReceived",
            Dimensions=[{"Name": "QueueName", "Value": queue_name}],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=days),
            EndTime=datetime.datetime.utcnow(),
            Period=ONE_DAY_IN_SECONDS,
            Statistics=["Sum"],
        )

        datapoints = response.get("Datapoints", [])
        datapoints.sort(key=lambda x: x["Timestamp"])

        metrics = {
            "queue_name": queue_name,
            "metric": "NumberOfMessagesReceived",
            "period": "last_7_days",
            "total": sum(point["Sum"] for point in datapoints),
            "daily_data": [
                {"date": point["Timestamp"].strftime("%Y-%m-%d"), "value": int(point["Sum"])} for point in datapoints
            ],
        }

        return metrics

    except ClientError as e:
        raise ValueError(f"Failed to get queue metrics: {e}") from e


def get_queue_attributes(sqs_client, queue_url):
    """Get all attributes of a specific queue.

    Args:
        sqs_client: boto3 SQS client object
        queue_url: The URL of the queue to get attributes for

    Returns:
        dict: Dictionary containing queue attributes with friendly names and values

    Raises:
        ValueError: When AWS API call fails
    """
    try:
        response = sqs_client.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])

        attributes = response.get("Attributes", {})

        friendly_attributes = {
            "Created": attributes.get("CreatedTimestamp", "N/A"),
            "Messages Available": attributes.get("ApproximateNumberOfMessages", "N/A"),
            "Messages In Flight": attributes.get("ApproximateNumberOfMessagesNotVisible", "N/A"),
            "Messages Delayed": attributes.get("ApproximateNumberOfMessagesDelayed", "N/A"),
            "Message Retention Period (days)": str(int(attributes.get("MessageRetentionPeriod", 0)) / 86400),
            "Maximum Message Size (KB)": str(int(attributes.get("MaximumMessageSize", 0)) / 1024),
            "Visibility Timeout (seconds)": attributes.get("VisibilityTimeout", "N/A"),
            "Receive Message Wait Time (seconds)": attributes.get("ReceiveMessageWaitTimeSeconds", "N/A"),
            "Dead Letter Target": attributes.get("RedrivePolicy", "None"),
            "KMS Master Key": attributes.get("KmsMasterKeyId", "None"),
            "KMS Data Key Reuse Period": attributes.get("KmsDataKeyReusePeriod", "N/A"),
            "Content Based Deduplication": attributes.get("ContentBasedDeduplication", "False"),
            "Deduplication Scope": attributes.get("DeduplicationScope", "N/A"),
            "FIFO Queue": attributes.get("FifoQueue", "False"),
            "Policy": attributes.get("Policy", "None"),
        }

        return friendly_attributes

    except ClientError as e:
        raise ValueError(f"Failed to get queue attributes: {e}") from e
