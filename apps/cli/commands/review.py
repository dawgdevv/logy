import typer
from rich.console import Console

from packages.database.repository import Repository
from packages.shared.config import settings

app = typer.Typer()
console = Console()
repo = Repository(settings.db_path)


@app.command()
def weekly() -> None:
    """Generate a weekly review."""
    entries = repo.get_entries(limit=100)
    if not entries:
        console.print("[yellow]No entries to review.[/yellow]")
        return

    projects: dict[str, list[str]] = {}
    for entry in entries:
        pname = entry.project.name if entry.project else "Uncategorized"
        if pname not in projects:
            projects[pname] = []
        projects[pname].append(entry.content)

    console.print("\n[bold]Weekly Review[/bold]\n")
    for project, items in projects.items():
        console.print(f"  [cyan]{project}[/cyan] ({len(items)} entries)")
        for item in items[:5]:
            console.print(f"    • {item[:80]}")
        if len(items) > 5:
            console.print(f"    [dim]... and {len(items) - 5} more[/dim]")
        console.print()
