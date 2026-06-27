
import typer
from rich.console import Console
from rich.table import Table

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import CATEGORIES, Difficulty

app = typer.Typer()
console = Console()
repo = Repository(settings.db_path)


@app.command()
def create(
    content: str = typer.Argument(..., help="What did you build today?"),
    project: str | None = typer.Option(None, "--project", "-p", help="Project name"),
    category: str = typer.Option(
        "other", "--category", "-c", help=f"Category: {', '.join(CATEGORIES)}"
    ),
    difficulty: Difficulty = typer.Option(
        Difficulty.medium, "--difficulty", "-d", help="Difficulty level"
    ),
    tags: str | None = typer.Option(None, "--tags", "-t", help="Comma-separated tags"),
) -> None:
    """Log today's work."""
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    entry = repo.create_entry(
        content=content,
        project_name=project,
        category=category,
        difficulty=difficulty,
        tags=tag_list,
    )
    console.print(f"[green]✓[/green] Logged entry #{entry.id}")


@app.command()
def list(
    limit: int = typer.Option(50, "--limit", "-l", help="Number of entries"),
) -> None:
    """List recent entries."""
    entries = repo.get_entries(limit=limit)
    if not entries:
        console.print("[yellow]No entries found.[/yellow]")
        return

    table = Table(title="Recent Entries")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Content")
    table.add_column("Project")
    table.add_column("Difficulty")

    for entry in entries:
        date_str = entry.created_at.strftime("%Y-%m-%d %H:%M")
        diff_style = {
            Difficulty.easy: "green",
            Difficulty.medium: "yellow",
            Difficulty.hard: "red",
        }.get(entry.difficulty, "white")
        project_name = entry.project.name if entry.project else ""
        table.add_row(
            str(entry.id),
            date_str,
            entry.content[:80],
            project_name,
            f"[{diff_style}]{entry.difficulty.value}[/{diff_style}]",
        )

    console.print(table)
