
import typer
from rich.console import Console
from rich.table import Table

from packages.database.repository import Repository
from packages.shared.config import settings

app = typer.Typer()
console = Console()
repo = Repository(settings.db_path)


@app.command()
def list() -> None:
    """List all projects."""
    projects = repo.get_projects()
    if not projects:
        console.print("[yellow]No projects yet.[/yellow]")
        return

    table = Table(title="Projects")
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Entries")
    table.add_column("Last Updated")

    for project in projects:
        entry_count = len(project.entries)
        table.add_row(
            str(project.id),
            project.name,
            str(entry_count),
            project.updated_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


@app.command()
def timeline(
    project_name: str = typer.Argument(..., help="Project name"),
) -> None:
    """Show a project's timeline."""
    project = repo.get_project_by_name(project_name)
    if not project:
        console.print(f"[red]Project '{project_name}' not found.[/red]")
        return

    entries = sorted(project.entries, key=lambda e: e.created_at)
    console.print(f"\n[bold]{project.name}[/bold] — Timeline\n")
    for entry in entries:
        date_str = entry.created_at.strftime("%b %d, %Y")
        console.print(f"  [dim]{date_str}[/dim]  {entry.content[:100]}")
    console.print()
