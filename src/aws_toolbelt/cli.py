import typer
from rich.console import Console

from aws_toolbelt import __version__
from aws_toolbelt.aws_sqs import (
    analyze_queue_volume,
    create_sqs_connection,
    get_queue_attributes,
    get_queue_metrics,
    get_queue_oldest_message,
    list_sqs_queues,
)
from aws_toolbelt.cli_helpers import panel as gui_panel
from aws_toolbelt.cli_helpers import text as gui_text

app = typer.Typer(
    name="aws-toolbelt",
    help="A CLI tool for managing AWS resources",
    add_completion=True,
)
console = Console()


@app.command()
def hello(
    name: str = typer.Option("World", "--name", "-n", help="Name to greet"),
) -> None:
    panel_content = gui_text(f"Hello, {name}!")
    panel = gui_panel(panel_content, "AWS Toolbelt Greeting")
    console.print(panel)

    info_text = gui_text("")
    info_text.append("This is AWS Toolbelt v", style="dim")
    info_text.append(__version__, style="bold")
    info_text.append(" - Your AWS metrics extraction tool!", style="dim")

    console.print("\n")
    console.print(info_text, justify="center")


@app.command()
def sqs_list_queues(
    queue_name_prefix: str = typer.Option(None, "--name", "-n", help="Filter queues by name prefix"),
) -> None:
    panel_content = gui_text(f"Listing queues with prefix: {queue_name_prefix}")
    panel = gui_panel(panel_content, "AWS SQS Queues")
    console.print(panel)

    sqs_client = create_sqs_connection()
    queues = list_sqs_queues(sqs_client, queue_name_prefix)

    for queue in queues:
        queue_text = f"Name: {queue['name']}\nURL: {queue['url']}"
        console.print(gui_text(queue_text))


@app.command()
def sqs_get_attributes(
    queue_name: str = typer.Argument(..., help="The name of the queue to get attributes for"),
) -> None:
    """Get all attributes of a specific SQS queue."""
    panel_content = gui_text(f"Getting attributes for queue: {queue_name}")
    panel = gui_panel(panel_content, "AWS SQS Queue Attributes")
    console.print(panel)

    sqs_client = create_sqs_connection()

    queues = list_sqs_queues(sqs_client)
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(gui_text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    attributes = get_queue_attributes(sqs_client, queue_url)

    for key, value in attributes.items():
        console.print(gui_text(f"{key}: {value}"))


@app.command()
def sqs_get_metrics(
    queue_name: str = typer.Argument(..., help="The name of the queue to get metrics for"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Get CloudWatch metrics for a specific SQS queue."""
    panel_content = gui_text(f"Getting metrics for queue: {queue_name} (last {days} days)")
    panel = gui_panel(panel_content, "AWS SQS Queue Metrics")
    console.print(panel)

    sqs_client = create_sqs_connection()

    # Primeiro, encontrar a URL da fila pelo nome
    queues = list_sqs_queues(sqs_client)
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(gui_text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    metrics = get_queue_metrics(sqs_client, queue_url, days)

    console.print(gui_text(f"\nTotal messages received: {metrics['total']:,}", style="bold blue"))

    console.print(gui_text("\nDaily breakdown:", style="bold"))
    for day in metrics["daily_data"]:
        console.print(gui_text(f"{day['date']}: {day['value']:,} messages"))

    # Criar gráfico ASCII
    console.print(gui_text("\nMessage Volume Chart:", style="bold"))

    # Encontrar o valor máximo para escala
    max_value = max(day["value"] for day in metrics["daily_data"])
    if max_value == 0:
        max_value = 1  # Evitar divisão por zero

    # Definir altura do gráfico
    height = 8
    scale_factor = height / max_value

    # Preparar dados para o gráfico
    date_width = 8  # Largura para cada data no eixo X
    y_axis_width = 10  # Largura para os valores do eixo Y
    graph_width = len(metrics["daily_data"]) * date_width

    # Criar barras e coletar datas
    bars = []
    dates = []
    for day in metrics["daily_data"]:
        date = day["date"].split("-")[1:]  # Remove o ano
        date_label = f"{date[0]}-{date[1]}"
        dates.append(date_label)

        # Calcular altura da barra
        bar_height = int(day["value"] * scale_factor)
        if day["value"] > 0 and bar_height == 0:
            bar_height = 1  # Garantir que valores pequenos sejam visíveis

        # Criar a barra
        bar = []
        for h in range(height):
            if h >= (height - bar_height):
                bar.append("█")
            else:
                bar.append(" ")
        bars.append(bar)

    # Construir o gráfico linha por linha
    graph_lines = []

    # Adicionar escala Y e barras
    max_value / 4
    for i in range(height):
        # Determinar se esta linha precisa de um marcador Y
        y_index = height - i - 1
        if y_index == height - 1:
            y_value = f"{int(max_value):,} ┬"
        elif y_index == 0:
            y_value = f"{0:,} ┴"
        elif y_index % 2 == 0:
            y_value = f"{int((y_index / height) * max_value):,} ┤"
        else:
            y_value = " " * (y_axis_width - 2) + "│"

        # Construir a linha com o valor Y e as barras
        bar_line = ""
        for bar in bars:
            bar_line += bar[i] + " " * (date_width - 1)

        graph_lines.append(f"{y_value:>{y_axis_width}}{bar_line}")

    # Adicionar linha base do eixo X
    x_axis = "─" * graph_width
    graph_lines.append(f"{' ' * (y_axis_width - 1)}└{x_axis}")

    # Adicionar datas no eixo X
    x_labels = ""
    for date in dates:
        x_labels += f"{date:<{date_width}}"
    graph_lines.append(f"{' ' * y_axis_width}{x_labels}")

    # Adicionar valores
    values = ""
    for day in metrics["daily_data"]:
        values += f"({day['value']:,})" + " " * (date_width - len(f"({day['value']:,})"))
    graph_lines.append(f"{' ' * y_axis_width}{values}")

    # Imprimir o gráfico
    console.print()
    for line in graph_lines:
        console.print(gui_text(line, style="dim" if "└" in line or not any(c in "┬┤┴│" for c in line) else None))


@app.command()
def sqs_get_oldest_message(
    queue_name: str = typer.Argument(..., help="The name of the queue to check"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Get the age of the oldest message in a specific SQS queue over time."""
    panel_content = gui_text(f"Getting oldest message age for queue: {queue_name} (last {days} days)")
    panel = gui_panel(panel_content, "AWS SQS Queue Message Age")
    console.print(panel)

    sqs_client = create_sqs_connection()

    queues = list_sqs_queues(sqs_client)
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(gui_text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    metrics = get_queue_oldest_message(sqs_client, queue_url, days)

    console.print(gui_text("\nSummary:", style="bold"))
    console.print(gui_text(f"Current oldest message age: {metrics['current_max_age']}", style="bold blue"))
    console.print(gui_text(f"Maximum age in period: {metrics['period_max_age']}", style="bold blue"))


@app.command()
def sqs_analyze_volume(
    queue_name: str = typer.Argument(..., help="The name of the queue to analyze"),
    days: int = typer.Option(15, "--days", "-d", help="Number of days to look back"),
) -> None:
    """Analyze message volume trends for a specific SQS queue."""
    panel_content = gui_text(f"Analyzing message volume for queue: {queue_name} (last {days} days)")
    panel = gui_panel(panel_content, "AWS SQS Queue Volume Analysis")
    console.print(panel)

    sqs_client = create_sqs_connection()

    # Primeiro, encontrar a URL da fila pelo nome
    queues = list_sqs_queues(sqs_client)
    queue_url = None
    for queue in queues:
        if queue["name"] == queue_name:
            queue_url = queue["url"]
            break

    if not queue_url:
        console.print(gui_text(f"Queue '{queue_name}' not found", style="bold red"))
        return

    # Analisar o volume de mensagens
    analysis = analyze_queue_volume(sqs_client, queue_url, days)

    # Exibir análise
    console.print()
    console.print(gui_text("Volume Analysis:", style="bold"))

    # Dia com maior volume
    console.print(gui_text("• Peak Volume Day:", style="bold blue"))
    console.print(gui_text(f"  - Date: {analysis['max_volume_day']}", style="dim"))
    console.print(gui_text(f"  - Volume: {analysis['max_volume']:,} messages"))

    # Comparação com segundo maior
    if analysis["second_max_day"]:
        console.print()
        console.print(gui_text("• Comparison with Second Highest:", style="bold blue"))
        console.print(gui_text(f"  - Second Highest Day: {analysis['second_max_day']}", style="dim"))
        console.print(gui_text(f"  - Second Highest Volume: {analysis['second_max_volume']:,} messages"))
        console.print(gui_text(f"  - Volume Difference: +{analysis['volume_difference']:,} messages"))
        console.print(gui_text(f"  - Percentage Increase: {analysis['volume_increase_percent']:.1f}%"))

    # Comparação com média
    console.print()
    console.print(gui_text("• Comparison with Mean:", style="bold blue"))
    console.print(gui_text(f"  - Mean Volume: {int(analysis['mean_volume']):,} messages"))
    console.print(gui_text(f"  - Difference from Mean: +{int(analysis['mean_difference']):,} messages"))
    console.print(gui_text(f"  - Percentage Above Mean: {analysis['mean_increase_percent']:.1f}%"))

    # Comparação com mediana
    console.print()
    console.print(gui_text("• Comparison with Median:", style="bold blue"))
    console.print(gui_text(f"  - Median Volume: {int(analysis['median_volume']):,} messages"))
    console.print(gui_text(f"  - Difference from Median: +{int(analysis['median_difference']):,} messages"))
    console.print(gui_text(f"  - Percentage Above Median: {analysis['median_increase_percent']:.1f}%"))


if __name__ == "__main__":
    app()
