import typer
from rich.console import Console

from apps.tui.app import main as tui_main

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)
def start() -> None:
    """Launch the Textual TUI."""
    tui_main()
