import typer
from rich.console import Console

from aws_toolbelt import __version__
from aws_toolbelt.aws_sqs import (
    analyze_queue_volume,
    get_queue_attributes,
    get_queue_metrics,
    get_queue_oldest_message,
    list_sqs_queues,
)
from aws_toolbelt.cli_helpers import (
    Panel,
    Text,
    create_bar_chart,
    create_daily_breakdown,
)

app = typer.Typer(
    name="aws-toolbelt",
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
        aws-toolbelt sqs-list-queues

        # List queues with specific prefix
        aws-toolbelt sqs-list-queues --name "prod-"
        aws-toolbelt sqs-list-queues -n "dev-"

        # List queues with full prefix
        aws-toolbelt sqs-list-queues --name "my-app-queue"
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
        aws-toolbelt sqs-get-attributes "my-queue"

        # Get attributes for queue with special characters
        aws-toolbelt sqs-get-attributes "prod-queue-123"

        # Get attributes for FIFO queue
        aws-toolbelt sqs-get-attributes "my-fifo-queue.fifo"
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
        aws-toolbelt sqs-get-metrics "my-queue"

        # Get metrics for last 14 days
        aws-toolbelt sqs-get-metrics "my-queue" --days 14
        aws-toolbelt sqs-get-metrics "my-queue" -d 14

        # Get metrics for last 30 days
        aws-toolbelt sqs-get-metrics "prod-queue" --days 30

        # Get metrics for last 3 days
        aws-toolbelt sqs-get-metrics "dev-queue" -d 3
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
        data=metrics["daily_data"],
        value_key="value",
        date_key="date",
        message_suffix="messages"
    )
    for line in breakdown_lines:
        console.print(line)

    console.print(Text("\nMessage Volume Chart:", style="bold"))

    graph_lines = create_bar_chart(
        data=metrics["daily_data"],
        value_key="value",
        label_key="date",
        title="Message Volume Chart"
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
        aws-toolbelt sqs-get-oldest-message "my-queue"

        # Get oldest message age for last 14 days
        aws-toolbelt sqs-get-oldest-message "my-queue" --days 14
        aws-toolbelt sqs-get-oldest-message "my-queue" -d 14

        # Get oldest message age for last 30 days
        aws-toolbelt sqs-get-oldest-message "prod-queue" --days 30

        # Get oldest message age for last 24 hours
        aws-toolbelt sqs-get-oldest-message "dev-queue" -d 1
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
        aws-toolbelt sqs-analyze-volume "my-queue"

        # Analyze multiple queues for last 15 days
        aws-toolbelt sqs-analyze-volume "queue1" "queue2" "queue3"

        # Analyze queues for last 30 days
        aws-toolbelt sqs-analyze-volume "prod-queue" "dev-queue" --days 30
        aws-toolbelt sqs-analyze-volume "prod-queue" "dev-queue" -d 30

        # Analyze queues for last 7 days
        aws-toolbelt sqs-analyze-volume "my-queue" -d 7

        # Analyze multiple queues with different time periods
        aws-toolbelt sqs-analyze-volume "high-volume-queue" "low-volume-queue" --days 60
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

        console.print(Text("\nDaily breakdown:", style="bold"))
        breakdown_lines = create_daily_breakdown(
            data=analysis["daily_data"],
            value_key="value",
            date_key="date",
            message_suffix="messages"
        )
        for line in breakdown_lines:
            console.print(line)

        console.print(Text("\nMessage Volume Chart:", style="bold"))
        graph_lines = create_bar_chart(
            data=analysis["daily_data"],
            value_key="value",
            label_key="date",
            title="Message Volume Chart"
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


if __name__ == "__main__":
    app()
