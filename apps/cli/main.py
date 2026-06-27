import typer

from apps.cli.commands import log, projects, review, search, serve

app = typer.Typer(
    name="logy",
    help="Terminal-first professional memory for builders.",
)

app.add_typer(log.app, name="log", help="Log today's work")
app.add_typer(search.app, name="search", help="Search entries")
app.add_typer(projects.app, name="projects", help="Manage projects")
app.add_typer(serve.app, name="serve", help="Start the web dashboard")
app.add_typer(review.app, name="review", help="Generate weekly review")


if __name__ == "__main__":
    app()
