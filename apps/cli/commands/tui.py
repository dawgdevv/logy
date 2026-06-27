import typer
from rich.console import Console

from apps.tui.app import main as tui_main

app = typer.Typer()
console = Console()


@app.command()
def start() -> None:
    """Launch the Textual TUI."""
    tui_main()
