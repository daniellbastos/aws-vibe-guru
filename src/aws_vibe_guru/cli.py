import json

import typer
from rich.console import Console

from aws_vibe_guru.aws_s3 import (
    get_object_info,
    list_bucket_objects,
    list_buckets,
    read_folder_contents,
    read_object_content,
)
from aws_vibe_guru.aws_sqs import (
    analyze_queue_volume,
    get_queue_attributes,
    get_queue_metrics,
    get_queue_oldest_message,
    list_sqs_queues,
)
from aws_vibe_guru.cli_helpers import (
    Panel,
    Text,
    create_bar_chart,
    create_daily_breakdown,
)

app = typer.Typer(
    name="aws-vibe-guru",
    help="A CLI tool for managing AWS resources",
    add_completion=True,
)
console = Console()


@app.command()
def sqs_list_queues(
    queue_name_prefix: str = typer.Option(None, "--name", "-n", help="Filter queues by name prefix"),
) -> None:
    """List all SQS queues with optional filtering by name prefix.

    Examples:
        # List all queues
        aws-vibe-guru sqs-list-queues

        # List queues with specific prefix
        aws-vibe-guru sqs-list-queues --name "prod-"
        aws-vibe-guru sqs-list-queues -n "dev-"

        # List queues with full prefix
        aws-vibe-guru sqs-list-queues --name "my-app-queue"
    """
    panel_content = Text(f"Listing queues with prefix: {queue_name_prefix}")
    panel = Panel(panel_content, "AWS SQS Queues")
    console.print(panel)

    queues = list_sqs_queues(queue_name_prefix)

    for queue in queues:
        queue_text = f"Name: {queue['name']}\nURL: {queue['url']}"
        console.print(Text(queue_text))


@app.command()
def sqs_get_attributes(
    queue_name: str = typer.Argument(..., help="The name of the queue to get attributes for"),
) -> None:
    """Get all attributes of a specific SQS queue.

    Examples:
        # Get attributes for a specific queue
        aws-vibe-guru sqs-get-attributes "my-queue"

        # Get attributes for queue with special characters
        aws-vibe-guru sqs-get-attributes "prod-queue-123"

        # Get attributes for FIFO queue
        aws-vibe-guru sqs-get-attributes "my-fifo-queue.fifo"
    """
    panel_content = Text(f"Getting attributes for queue: {queue_name}")
    panel = Panel(panel_content, "AWS SQS Queue Attributes")
    console.print(panel)

    queues = list_sqs_queues()
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(Text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    attributes = get_queue_attributes(queue_url)

    for key, value in attributes.items():
        console.print(Text(f"{key}: {value}"))


@app.command()
def sqs_get_metrics(
    queue_name: str = typer.Argument(..., help="The name of the queue to get metrics for"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Get CloudWatch metrics for a specific SQS queue.

    Examples:
        # Get metrics for last 7 days (default)
        aws-vibe-guru sqs-get-metrics "my-queue"

        # Get metrics for last 14 days
        aws-vibe-guru sqs-get-metrics "my-queue" --days 14
        aws-vibe-guru sqs-get-metrics "my-queue" -d 14

        # Get metrics for last 30 days
        aws-vibe-guru sqs-get-metrics "prod-queue" --days 30

        # Get metrics for last 3 days
        aws-vibe-guru sqs-get-metrics "dev-queue" -d 3
    """
    panel_content = Text(f"Getting metrics for queue: {queue_name} (last {days} days)")
    panel = Panel(panel_content, "AWS SQS Queue Metrics")
    console.print(panel)

    queues = list_sqs_queues()
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(Text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    metrics = get_queue_metrics(queue_url, days)

    console.print(Text(f"\nTotal messages received: {metrics['total']:,}", style="bold blue"))

    console.print(Text("\nDaily breakdown:", style="bold"))
    breakdown_lines = create_daily_breakdown(
        data=metrics["daily_data"], value_key="value", date_key="date", message_suffix="messages"
    )
    for line in breakdown_lines:
        console.print(line)

    console.print(Text("\nMessage Volume Chart:", style="bold"))

    graph_lines = create_bar_chart(
        data=metrics["daily_data"], value_key="value", label_key="date", title="Message Volume Chart"
    )

    console.print()
    for line in graph_lines:
        console.print(Text(line, style="dim" if "└" in line or not any(c in "┬┤┴│" for c in line) else None))


@app.command()
def sqs_get_oldest_message(
    queue_name: str = typer.Argument(..., help="The name of the queue to check"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Get the age of the oldest message in a specific SQS queue over time.

    Examples:
        # Get oldest message age for last 7 days (default)
        aws-vibe-guru sqs-get-oldest-message "my-queue"

        # Get oldest message age for last 14 days
        aws-vibe-guru sqs-get-oldest-message "my-queue" --days 14
        aws-vibe-guru sqs-get-oldest-message "my-queue" -d 14

        # Get oldest message age for last 30 days
        aws-vibe-guru sqs-get-oldest-message "prod-queue" --days 30

        # Get oldest message age for last 24 hours
        aws-vibe-guru sqs-get-oldest-message "dev-queue" -d 1
    """
    panel_content = Text(f"Getting oldest message age for queue: {queue_name} (last {days} days)")
    panel = Panel(panel_content, "AWS SQS Queue Message Age")
    console.print(panel)

    queues = list_sqs_queues()
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(Text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    metrics = get_queue_oldest_message(queue_url, days)

    console.print(Text("\nSummary:", style="bold"))
    console.print(Text(f"Current oldest message age: {metrics['current_max_age']}", style="bold blue"))
    console.print(Text(f"Maximum age in period: {metrics['period_max_age']}", style="bold blue"))


@app.command()
def sqs_analyze_volume(
    queue_names: list[str] = typer.Argument(..., help="Names of the queues to analyze"),
    days: int = typer.Option(15, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Analyze message volume trends for multiple SQS queues.

    Examples:
        # Analyze single queue for last 15 days (default)
        aws-vibe-guru sqs-analyze-volume "my-queue"

        # Analyze multiple queues for last 15 days
        aws-vibe-guru sqs-analyze-volume "queue1" "queue2" "queue3"

        # Analyze queues for last 30 days
        aws-vibe-guru sqs-analyze-volume "prod-queue" "dev-queue" --days 30
        aws-vibe-guru sqs-analyze-volume "prod-queue" "dev-queue" -d 30

        # Analyze queues for last 7 days
        aws-vibe-guru sqs-analyze-volume "my-queue" -d 7

        # Analyze multiple queues with different time periods
        aws-vibe-guru sqs-analyze-volume "high-volume-queue" "low-volume-queue" --days 60
    """
    panel_content = Text(f"Analyzing message volume for {len(queue_names)} queues (last {days} days)")
    panel = Panel(panel_content, "AWS SQS Queue Volume Analysis")
    console.print(panel)

    all_queues = list_sqs_queues()

    map_queue_url = {queue["name"]: queue["url"] for queue in all_queues if queue["name"] in queue_names}

    for queue_name in queue_names:
        queue_url = map_queue_url.get(queue_name)

        if not queue_url:
            console.print(Text(f"\nQueue '{queue_name}' not found", style="bold red"))
            continue

        analysis = analyze_queue_volume(queue_url, days)

        console.print()
        console.print(Text(f"Queue: {queue_name}", style="bold green"))
        console.print(Text("─" * (len(queue_name) + 7), style="dim"))

        total_messages = sum(day["value"] for day in analysis["daily_data"])
        console.print(Text(f"Total messages received: {total_messages:,}", style="bold blue"))

        console.print(Text("\nDaily breakdown (top 3 days highlighted):", style="bold"))
        breakdown_lines = create_daily_breakdown(
            data=analysis["daily_data"],
            value_key="value",
            date_key="date",
            message_suffix="messages",
            number_of_days_to_highlight=3,
        )
        for line in breakdown_lines:
            console.print(line)

        console.print(Text("\nMessage Volume Chart:", style="bold"))
        graph_lines = create_bar_chart(
            data=analysis["daily_data"], value_key="value", label_key="date", title="Message Volume Chart"
        )

        console.print()
        for line in graph_lines:
            console.print(Text(line, style="dim" if "└" in line or not any(c in "┬┤┴│" for c in line) else None))

        console.print()
        console.print(Text("Volume Analysis:", style="bold"))

        console.print(Text("• Peak Volume Day:", style="bold blue"))
        console.print(Text(f"  - Date: {analysis['max_volume_day']}", style="dim"))
        console.print(Text(f"  - Volume: {analysis['max_volume']:,} messages"))

        if analysis["second_max_day"]:
            console.print()
            console.print(Text("• Comparison with Second Highest:", style="bold blue"))
            console.print(Text(f"  - Second Highest Day: {analysis['second_max_day']}", style="dim"))
            console.print(Text(f"  - Second Highest Volume: {analysis['second_max_volume']:,} messages"))
            console.print(Text(f"  - Volume Difference: +{analysis['volume_difference']:,} messages"))
            console.print(Text(f"  - Percentage Increase: {analysis['volume_increase_percent']:.1f}%"))

        console.print()
        console.print(Text("• Comparison with Mean:", style="bold blue"))
        console.print(Text(f"  - Mean Volume: {int(analysis['mean_volume']):,} messages"))
        console.print(Text(f"  - Difference from Mean: +{int(analysis['mean_difference']):,} messages"))
        console.print(Text(f"  - Percentage Above Mean: {analysis['mean_increase_percent']:.1f}%"))

        console.print()
        console.print(Text("• Comparison with Median:", style="bold blue"))
        console.print(Text(f"  - Median Volume: {int(analysis['median_volume']):,} messages"))
        console.print(Text(f"  - Difference from Median: +{int(analysis['median_difference']):,} messages"))
        console.print(Text(f"  - Percentage Above Median: {analysis['median_increase_percent']:.1f}%"))


@app.command()
def s3_list_buckets() -> None:
    """List all S3 buckets in the AWS account.

    Examples:
        aws-vibe-guru s3-list-buckets
    """
    panel_content = Text("Listing all S3 buckets")
    panel = Panel(panel_content, "AWS S3 Buckets")
    console.print(panel)

    buckets = list_buckets()

    if not buckets:
        console.print(Text("No buckets found", style="bold yellow"))
        return

    console.print(Text(f"\nTotal buckets: {len(buckets)}", style="bold blue"))
    console.print()

    for bucket in buckets:
        bucket_text = f"Name: {bucket['name']}\nCreated: {bucket['creation_date']}"
        console.print(Text(bucket_text))
        console.print()


@app.command()
def s3_list_objects(
    bucket_name: str = typer.Argument(..., help="The name of the bucket to list objects from"),
    prefix: str = typer.Option(None, "--prefix", "-p", help="Filter objects by prefix (file path)"),
    max_results: int = typer.Option(
        None, "--max", "-m", help="Maximum number of objects to return (default: unlimited)"
    ),
    summary: bool = typer.Option(
        False, "--summary", "-s", help="Show only summary information (bucket, filter, total)"
    ),
) -> None:
    """List all objects in a specific S3 bucket with optional prefix filtering.

    Examples:
        aws-vibe-guru s3-list-objects "my-bucket"

        aws-vibe-guru s3-list-objects "my-bucket" --prefix "logs/"
        aws-vibe-guru s3-list-objects "my-bucket" -p "data/2024/"

        aws-vibe-guru s3-list-objects "my-bucket" --max 500
        aws-vibe-guru s3-list-objects "my-bucket" -m 100

        aws-vibe-guru s3-list-objects "my-bucket" --prefix "reports/" --max 50

        aws-vibe-guru s3-list-objects "my-bucket" --summary
        aws-vibe-guru s3-list-objects "my-bucket" -s
    """
    prefix_text = f" with prefix: {prefix}" if prefix else ""
    panel_content = Text(f"Listing objects in bucket: {bucket_name}{prefix_text}")
    panel = Panel(panel_content, "AWS S3 Bucket Objects")
    console.print(panel)

    try:
        result = list_bucket_objects(bucket_name, prefix, max_results)

        console.print(Text(f"\nBucket: {result['bucket_name']}", style="bold green"))
        console.print(Text(f"Filter: {result['prefix']}", style="bold green"))
        console.print(Text(f"Total objects: {result['total_objects']:,}", style="bold blue"))

        if summary:
            return

        if result["total_objects"] == 0:
            console.print(Text("\nNo objects found", style="bold yellow"))
            return

        console.print(Text("\nObjects:", style="bold"))
        console.print()

        for obj in result["objects"]:
            obj_text = (
                f"Key: {obj['key']}\n"
                f"Size: {obj['size']:,} bytes ({obj['size_mb']} MB)\n"
                f"Last Modified: {obj['last_modified']}\n"
                f"Storage Class: {obj['storage_class']}"
            )
            console.print(Text(obj_text))
            console.print()

    except ValueError as e:
        console.print(Text(f"Error: {str(e)}", style="bold red"))


@app.command()
def s3_get_object(
    bucket_name: str = typer.Argument(..., help="The name of the bucket"),
    object_key: str = typer.Argument(..., help="The key (path) of the object"),
) -> None:
    """Get detailed information about a specific object in an S3 bucket.

    Examples:
        aws-vibe-guru s3-get-object "my-bucket" "file.txt"

        aws-vibe-guru s3-get-object "my-bucket" "logs/2024/app.log"

        aws-vibe-guru s3-get-object "data-bucket" "data/users/export.csv"
    """
    panel_content = Text(f"Getting object info: {object_key} from bucket: {bucket_name}")
    panel = Panel(panel_content, "AWS S3 Object Information")
    console.print(panel)

    try:
        obj_info = get_object_info(bucket_name, object_key)

        console.print()
        console.print(Text("Object Details:", style="bold green"))
        console.print(Text("─" * 50, style="dim"))
        console.print()

        console.print(Text(f"Bucket: {obj_info['bucket']}", style="bold blue"))
        console.print(Text(f"Key: {obj_info['key']}", style="bold blue"))
        console.print(Text(f"Size: {obj_info['size']:,} bytes ({obj_info['size_mb']} MB)"))
        console.print(Text(f"Last Modified: {obj_info['last_modified']}"))
        console.print(Text(f"Content Type: {obj_info['content_type']}"))
        console.print(Text(f"ETag: {obj_info['etag']}"))
        console.print(Text(f"Storage Class: {obj_info['storage_class']}"))
        console.print(Text(f"Version ID: {obj_info['version_id']}"))

        if obj_info["metadata"]:
            console.print()
            console.print(Text("Metadata:", style="bold"))
            for key, value in obj_info["metadata"].items():
                console.print(Text(f"  {key}: {value}"))

    except ValueError as e:
        console.print(Text(f"Error: {str(e)}", style="bold red"))


@app.command()
def s3_read_object(
    bucket_name: str = typer.Argument(..., help="The name of the bucket"),
    object_key: str = typer.Argument(None, help="The key (path) of the object to read"),
    prefix: str = typer.Option(None, "--prefix", "-p", help="Search for objects by prefix"),
    encoding: str = typer.Option("utf-8", "--encoding", "-e", help="Text encoding to use"),
    format_json: bool = typer.Option(False, "--json", "-j", help="Format JSON content with 2-space indentation"),
) -> None:
    """Read and display the content of a file from S3 bucket.

    Examples:
        aws-vibe-guru s3-read-object "my-bucket" "file.txt"

        aws-vibe-guru s3-read-object "my-bucket" "logs/2024/app.log"

        aws-vibe-guru s3-read-object "my-bucket" --prefix "config/"

        aws-vibe-guru s3-read-object "my-bucket" "file.txt" --encoding "latin-1"

        aws-vibe-guru s3-read-object "my-bucket" "data.json" --json
    """
    if not object_key and not prefix:
        console.print(Text("Error: Either object_key or --prefix must be provided", style="bold red"))
        return

    if prefix and not object_key:
        panel_content = Text(f"Searching objects in bucket: {bucket_name} with prefix: {prefix}")
        panel = Panel(panel_content, "AWS S3 Object Search")
        console.print(panel)

        try:
            result = list_bucket_objects(bucket_name, prefix)

            if result["total_objects"] == 0:
                console.print(Text(f"\nNo objects found with prefix '{prefix}'", style="bold yellow"))
                return

            console.print(Text(f"\nFound {result['total_objects']} object(s):", style="bold blue"))
            console.print()

            if result["total_objects"] == 1:
                object_key = result["objects"][0]["key"]
                console.print(Text(f"Reading: {object_key}", style="bold green"))
                console.print()
            else:
                console.print(
                    Text("Multiple objects found. Please specify the exact object_key:", style="bold yellow")
                )
                for obj in result["objects"]:
                    console.print(Text(f"  - {obj['key']}"))
                return

        except ValueError as e:
            console.print(Text(f"Error: {str(e)}", style="bold red"))
            return

    panel_content = Text(f"Reading object: {object_key} from bucket: {bucket_name}")
    panel = Panel(panel_content, "AWS S3 Object Content")
    console.print(panel)

    try:
        result = read_object_content(bucket_name, object_key, encoding)

        console.print()
        console.print(Text(f"Bucket: {result['bucket']}", style="bold blue"))
        console.print(Text(f"Key: {result['key']}", style="bold blue"))
        console.print(Text(f"Size: {result['size']:,} bytes", style="bold blue"))
        console.print(Text(f"Content Type: {result['content_type']}"))
        console.print(Text("─" * 80, style="dim"))
        console.print()

        if result["is_binary"]:
            console.print(
                Text("⚠️  This file appears to be binary and cannot be displayed as text.", style="bold yellow")
            )
            console.print(Text(f"File size: {result['size']:,} bytes", style="dim"))
        else:
            content_to_display = result["content"]

            if format_json:
                try:
                    json_data = json.loads(content_to_display)
                    content_to_display = json.dumps(json_data, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    console.print(
                        Text(
                            "⚠️  Warning: --json flag was used but content is not valid JSON. Displaying as-is.",
                            style="bold yellow",
                        )
                    )
                    console.print()

            console.print(content_to_display)

    except ValueError as e:
        console.print(Text(f"Error: {str(e)}", style="bold red"))


@app.command()
def s3_read_folder(
    bucket_name: str = typer.Argument(..., help="The name of the bucket"),
    prefix: str = typer.Argument(..., help="The folder prefix/path to read"),
    encoding: str = typer.Option("utf-8", "--encoding", "-e", help="Text encoding to use"),
    max_files: int = typer.Option(None, "--max", "-m", help="Maximum number of files to read (default: unlimited)"),
    format_json: bool = typer.Option(False, "--json", "-j", help="Format JSON content with 2-space indentation"),
) -> None:
    """Read all files from a folder in S3 bucket and display their contents.

    Examples:
        aws-vibe-guru s3-read-folder "my-bucket" "logs/2024/"

        aws-vibe-guru s3-read-folder "my-bucket" "config/" --json

        aws-vibe-guru s3-read-folder "my-bucket" "data/" --max 50

        aws-vibe-guru s3-read-folder "my-bucket" "files/" --encoding "latin-1"
    """
    try:
        result = read_folder_contents(bucket_name, prefix, encoding, max_files)

        console.print()
        console.print(Text(f"Reading folder: {prefix}", style="bold green"))
        console.print(Text(f"Bucket: {result['bucket']}", style="bold blue"))
        console.print(Text(f"Total files: {result['total_files']}", style="bold blue"))
        console.print(Text("=" * 80, style="dim"))
        console.print()

        if result["total_files"] == 0:
            console.print(Text("No files found in this folder", style="bold yellow"))
            return

        for file_data in result["files"]:
            console.print(Text(f"File: {file_data['key']}", style="bold cyan"))
            console.print(Text("-" * 80, style="dim"))

            if file_data["is_binary"]:
                console.print(Text("⚠️  Binary file (skipped)", style="yellow"))
                if "error" in file_data:
                    console.print(Text(f"Error: {file_data['error']}", style="red"))
            else:
                content_to_display = file_data["content"]

                if format_json:
                    try:
                        json_data = json.loads(content_to_display)
                        content_to_display = json.dumps(json_data, indent=2, ensure_ascii=False)
                    except json.JSONDecodeError:
                        pass

                console.print(content_to_display)

            console.print()

    except ValueError as e:
        console.print(Text(f"Error: {str(e)}", style="bold red"))


if __name__ == "__main__":
    app()
