from fastapi import APIRouter, HTTPException

from packages.database.repository import Repository
from packages.shared.config import settings
from packages.shared.constants import Difficulty

router = APIRouter(prefix="/entries", tags=["entries"])
repo = Repository(settings.db_path)


@router.get("/")
def list_entries(limit: int = 50, offset: int = 0):
    return repo.get_entries(limit=limit, offset=offset)


@router.get("/{entry_id}")
def get_entry(entry_id: int):
    entry = repo.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.post("/")
def create_entry(
    content: str,
    project: str | None = None,
    category: str = "other",
    difficulty: Difficulty = Difficulty.medium,
    tags: list[str] | None = None,
):
    return repo.create_entry(
        content=content,
        project_name=project,
        category=category,
        difficulty=difficulty,
        tags=tags,
    )
