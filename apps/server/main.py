from fastapi import FastAPI

from apps.server.api import entries, projects

app = FastAPI(title="Logy API", version="0.1.0")

app.include_router(entries.router)
app.include_router(projects.router)


@app.get("/health")
def health():
    return {"status": "ok"}
