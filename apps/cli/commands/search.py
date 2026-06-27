import typer
from rich.console import Console
from rich.table import Table

from packages.database.repository import Repository
from packages.shared.config import settings

app = typer.Typer()
console = Console()
repo = Repository(settings.db_path)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
) -> None:
    """Search entries by content."""
    entries = repo.search_entries(query)
    if not entries:
        console.print(f"[yellow]No entries matching '{query}'.[/yellow]")
        return

    table = Table(title=f"Results for '{query}'")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Content")
    table.add_column("Project")

    for entry in entries:
        project_name = entry.project.name if entry.project else ""
        table.add_row(
            str(entry.id),
            entry.created_at.strftime("%Y-%m-%d"),
            entry.content[:80],
            project_name,
        )

    console.print(table)
