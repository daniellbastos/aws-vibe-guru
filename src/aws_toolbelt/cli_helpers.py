from typing import Any, Tuple

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
