from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import FileResponse

from apps.server.api import entries, graph, projects
from apps.server.workers import start_worker

WEB_DIR = Path(__file__).parent.parent / "web" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_worker()
    yield


app = FastAPI(title="Logy API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(entries.router)
app.include_router(projects.router)
app.include_router(graph.router)


if WEB_DIR.exists():

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        file_path = WEB_DIR / full_path
        if full_path and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(WEB_DIR / "index.html")
