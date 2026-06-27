import shutil

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.text import Text

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import APP_VERSION, CATEGORIES, Difficulty

console = Console()
repo = Repository(settings.db_path)


def show_welcome() -> None:
    term = shutil.get_terminal_size()

    logo = Text(
        "  ▄▄▄      ▄▄▄  \n"
        "  ██   ██    ██   ██\n"
        "  ███████    ███████\n"
        "  ██   ██    ██   ██\n"
        "  ██   ██    ██   ██",
        style="cyan",
        no_wrap=True,
    )

    title = Text()
    title.append("logy", style="bold cyan")
    title.append(f"  v{APP_VERSION}", style="dim")

    question = Text("What did you work on today?", style="bold")

    option1 = Text("  [1]  Daily Log    —  What did you build or learn?")
    option2 = Text("  [2]  Project      —  Log work for a specific project")
    option3 = Text("  [3]  Hard Problem —  Solved something tough?")

    content = Group(
        logo,
        Text(""),
        title,
        Text(""),
        Text(""),
        question,
        Text(""),
        option1,
        option2,
        option3,
        Text(""),
    )

    console.clear()
    console.print(
        Panel(
            Align.center(content, vertical="middle"),
            box=box.ROUNDED,
            border_style="cyan",
            width=term.columns,
            height=term.lines,
        )
    )


def pick_option() -> int:
    console.print()
    choice = IntPrompt.ask("Choose", choices=["1", "2", "3"], default=1)
    return choice


def daily_log_flow() -> None:
    console.print("\n[bold cyan]Daily Log[/bold cyan] — What did you build or learn today?\n")
    content = Prompt.ask("Today's work", default="")
    if not content:
        console.print("[yellow]Nothing logged.[/yellow]")
        return

    project = Prompt.ask("Project (or press Enter to skip)", default="")
    category = _pick_category()
    difficulty = _pick_difficulty()
    tags_str = Prompt.ask("Tags (comma-separated, or press Enter to skip)", default="")

    tags = [t.strip() for t in tags_str.split(",")] if tags_str else None
    entry = repo.create_entry(
        content=content,
        project_name=project or None,
        category=category,
        difficulty=difficulty,
        tags=tags,
    )
    console.print(f"\n[green]✓[/green] Logged entry #{entry.id}\n")


def project_flow() -> None:
    console.print("\n[bold cyan]Project Log[/bold cyan]\n")
    projects = repo.get_projects()
    project_names = [p.name for p in projects]

    if project_names:
        console.print("[bold]Existing projects:[/bold]")
        for i, name in enumerate(project_names, 1):
            console.print(f"  [bold cyan]{i}[/]  {name}")
        console.print(f"  [bold cyan]{len(project_names) + 1}[/]  [dim]Create new project[/dim]")
        console.print()

        choice = IntPrompt.ask(
            "Select a project",
            choices=[str(i) for i in range(1, len(project_names) + 2)],
        )
        if choice == len(project_names) + 1:
            project_name = Prompt.ask("New project name")
        else:
            project_name = project_names[choice - 1]
    else:
        console.print("[yellow]No projects yet.[/yellow]")
        project_name = Prompt.ask("New project name")
        if not project_name:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    console.print(f"\nLogging for project: [bold cyan]{project_name}[/bold cyan]\n")
    content = Prompt.ask("What did you build?")
    if not content:
        console.print("[yellow]Nothing logged.[/yellow]")
        return

    category = _pick_category()
    difficulty = _pick_difficulty()
    tags_str = Prompt.ask("Tags (comma-separated, or press Enter to skip)", default="")

    tags = [t.strip() for t in tags_str.split(",")] if tags_str else None
    entry = repo.create_entry(
        content=content,
        project_name=project_name,
        category=category,
        difficulty=difficulty,
        tags=tags,
    )
    console.print(f"\n[green]✓[/green] Logged entry #{entry.id} to [bold]{project_name}[/bold]\n")


def hard_problem_flow() -> None:
    console.print("\n[bold cyan]Hard Problem[/bold cyan] — Solved something tough?\n")
    context = Prompt.ask("What was the problem?")
    if not context:
        console.print("[yellow]Nothing logged.[/yellow]")
        return

    solution = Prompt.ask("How did you solve it?")
    lessons = Prompt.ask("Lessons learned", default="")
    project = Prompt.ask("Project (or press Enter to skip)", default="")
    tags_str = Prompt.ask("Tags (comma-separated, or press Enter to skip)", default="")

    full_content = context
    if solution:
        full_content += f"\n\nSolution: {solution}"
    if lessons:
        full_content += f"\n\nLessons: {lessons}"

    tags = [t.strip() for t in tags_str.split(",")] if tags_str else None
    if tags:
        tags.append("hard-problem")
    else:
        tags = ["hard-problem"]

    entry = repo.create_entry(
        content=full_content,
        project_name=project or None,
        category="bugfix",
        difficulty=Difficulty.hard,
        tags=tags,
    )
    console.print(f"\n[green]✓[/green] Logged hard problem as entry #{entry.id}\n")


def _pick_category() -> str:
    console.print("\n[bold]Category:[/bold]")
    for i, cat in enumerate(CATEGORIES, 1):
        console.print(f"  [bold cyan]{i}[/]  {cat}")
    cats = [str(i) for i in range(1, len(CATEGORIES) + 1)]
    choice = IntPrompt.ask("Choose", choices=cats, default=1)
    return CATEGORIES[choice - 1]


def _pick_difficulty() -> Difficulty:
    console.print("\n[bold]Difficulty:[/bold]")
    console.print("  [bold cyan]1[/]  [green]Easy[/green]")
    console.print("  [bold cyan]2[/]  [yellow]Medium[/yellow]")
    console.print("  [bold cyan]3[/]  [red]Hard[/red]")
    choice = IntPrompt.ask("Choose", choices=["1", "2", "3"], default=2)
    return [Difficulty.easy, Difficulty.medium, Difficulty.hard][choice - 1]
