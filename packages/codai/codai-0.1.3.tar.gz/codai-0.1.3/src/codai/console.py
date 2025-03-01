# imports
import os
import pyperclip

from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory, InMemoryHistory

from codai.utils import get_codai_dir


# functions
def print(
    text: str, as_markdown: bool = True, as_panel: bool = True, header: str = "codai"
) -> None:
    """
    print text
    """
    # console
    console = Console()

    # style map
    style_map = {
        "user": "bold cyan",
        "codai": "bold violet",
    }

    if as_markdown:
        text = Markdown(text)

    if as_panel:
        text = Panel(text, title=header, border_style=style_map[header])

    console.print(text)


def clear() -> None:
    """
    clear the console
    """
    console = Console()
    console.clear()


def get_memory_history() -> InMemoryHistory:
    history = InMemoryHistory()
    return history


def get_file_history() -> FileHistory:
    history = FileHistory(os.path.join(get_codai_dir(), "chat.history"))
    return history


def get_input(prompt_text: str, history: FileHistory | InMemoryHistory) -> str:
    session = PromptSession(history=history)
    return session.prompt(prompt_text)
