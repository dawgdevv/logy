import typer
import uvicorn
from rich.console import Console

from packages.shared.config import settings

app = typer.Typer()
console = Console()


@app.command()
def start() -> None:
    """Start the FastAPI server and web dashboard."""
    addr = f"{settings.server_host}:{settings.server_port}"
    console.print(f"[green]Starting Logy server on {addr}[/green]")
    uvicorn.run(
        "apps.server.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
