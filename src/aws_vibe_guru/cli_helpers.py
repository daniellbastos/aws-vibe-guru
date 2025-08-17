from typing import Any, List, Tuple

from rich.panel import Panel as RichPanel
from rich.text import Text as RichText


class Text(RichText):
    """A Text class with default styling for CLI output."""

    def __init__(self, text: str, style: str = "bold green", **kwargs):
        super().__init__(text, style=style, **kwargs)


class Panel(RichPanel):
    """A Panel class with default styling for CLI output."""

    def __init__(
        self,
        content: Any,
        title: str,
        border_style: str = "blue",
        padding: Tuple[int, int] = (1, 2),
        **kwargs,
    ):
        super().__init__(
            content,
            title=title,
            border_style=border_style,
            padding=padding,
            **kwargs,
        )


def create_daily_breakdown(
    data: List[dict],
    value_key: str = "value",
    date_key: str = "date",
    message_suffix: str = "messages",
) -> List[Text]:
    """Create a daily breakdown display from data.

    Args:
        data: List of dictionaries containing the daily data
        value_key: Key in the dictionary for the numeric value
        date_key: Key in the dictionary for the date
        message_suffix: Suffix to append to the value (e.g., "messages", "requests")

    Returns:
        List of Text objects representing the daily breakdown lines
    """
    import datetime

    breakdown_lines = []

    for item in data:
        date_str = item[date_key]
        value = item[value_key]

        # Parse the date string to get the day of week
        try:
            if isinstance(date_str, str) and "-" in date_str:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                day_of_week = date_obj.strftime("%a")  # Abbreviated day name (Mon, Tue, etc.)
                formatted_date = f"[{day_of_week}] {date_str}"
            else:
                formatted_date = str(date_str)
        except ValueError:
            formatted_date = str(date_str)

        line_text = f"{formatted_date}: {value:,} {message_suffix}"
        breakdown_lines.append(Text(line_text))

    return breakdown_lines


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
