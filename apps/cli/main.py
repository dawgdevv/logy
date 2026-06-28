import threading

import typer
import uvicorn

from apps.cli.commands import log, projects, review, search, serve
from apps.cli.tui import run_interactive
from packages.shared.config import settings

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


def _start_server_background() -> None:
    uvicorn.run(
        "apps.server.main:app",
        host=settings.server_host,
        port=settings.server_port,
        log_level="error",
    )


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Terminal-first professional memory for builders."""
    if ctx.invoked_subcommand is not None:
        return

    server_thread = threading.Thread(target=_start_server_background, daemon=True)
    server_thread.start()

    run_interactive()


if __name__ == "__main__":
    app()
