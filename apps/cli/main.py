import typer

from apps.cli.commands import log, projects, review, search, serve
from apps.cli.interactive import run_interactive

app = typer.Typer(
    name="logy",
    help="Terminal-first professional memory for builders.",
    no_args_is_help=False,
    add_completion=False,
)

app.add_typer(log.app, name="log", help="Log today's work")
app.add_typer(search.app, name="search", help="Search entries")
app.add_typer(projects.app, name="projects", help="Manage projects")
app.add_typer(serve.app, name="serve", help="Start the web dashboard")
app.add_typer(review.app, name="review", help="Generate weekly review")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Terminal-first professional memory for builders."""
    if ctx.invoked_subcommand is not None:
        return
    run_interactive()


if __name__ == "__main__":
    app()
