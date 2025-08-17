from typing import Any, List, Tuple

from rich.panel import Panel
from rich.text import Text


def text(text: str, style: str = "bold green") -> Text:
    return Text(text, style=style)


def panel(
    content: Any,
    title: str,
    border_style: str = "blue",
    padding: Tuple[int, int] = (1, 2),
) -> Panel:
    return Panel(
        content,
        title=title,
        border_style=border_style,
        padding=padding,
    )


def create_bar_chart(
    data: List[dict],
    value_key: str = "value",
    label_key: str = "date",
    title: str = "Chart",
    height: int = 8,
    date_width: int = 8,
    y_axis_width: int = 10,
) -> List[str]:
    """Create an ASCII bar chart from data.

    Args:
        data: List of dictionaries containing the data points
        value_key: Key in the dictionary for the numeric value
        label_key: Key in the dictionary for the label
        title: Title for the chart
        height: Height of the chart in characters
        date_width: Width allocated for each data point
        y_axis_width: Width allocated for the y-axis

    Returns:
        List of strings representing the chart lines
    """
    if not data:
        return []

    max_value = max(item[value_key] for item in data)
    if max_value == 0:
        max_value = 1

    scale_factor = height / max_value
    graph_width = len(data) * date_width

    bars = []
    labels = []
    for item in data:
        label = item[label_key]
        if label_key == "date" and "-" in str(label):
            date_parts = str(label).split("-")[1:]
            label = f"{date_parts[0]}-{date_parts[1]}"
        labels.append(label)

        bar_height = int(item[value_key] * scale_factor)
        if item[value_key] > 0 and bar_height == 0:
            bar_height = 1

        bar = []
        for h in range(height):
            if h >= (height - bar_height):
                bar.append("█")
            else:
                bar.append(" ")
        bars.append(bar)

    # Calculate required y-axis width based on the largest formatted number
    max_formatted_value = f"{int(max_value):,}"
    y_axis_required_width = len(max_formatted_value) + 3  # +3 for " ┬", " ┴", " ┤"
    actual_y_axis_width = max(y_axis_width, y_axis_required_width)

    graph_lines = []

    for i in range(height):
        y_index = height - i - 1
        if y_index == height - 1:
            y_value = f"{int(max_value):,} ┬"
        elif y_index == 0:
            y_value = f"{0:,} ┴"
        elif y_index % 2 == 0:
            y_value = f"{int((y_index / height) * max_value):,} ┤"
        else:
            y_value = " " * (actual_y_axis_width - 2) + "│"

        bar_line = ""
        for bar in bars:
            bar_line += "  " + bar[i] + " " * (date_width - 3)

        graph_lines.append(f"{y_value:>{actual_y_axis_width}}{bar_line}")

    x_axis = "─" * graph_width
    graph_lines.append(f"{' ' * (actual_y_axis_width - 1)}└{x_axis}")

    x_labels = ""
    for label in labels:
        x_labels += f"{label:<{date_width}}"
    graph_lines.append(f"{' ' * actual_y_axis_width}{x_labels}")

    values = ""
    for item in data:
        values += " " * (date_width - len(f"{item[value_key]:,}"))
    graph_lines.append(f"{' ' * actual_y_axis_width}{values}")

    return graph_lines
