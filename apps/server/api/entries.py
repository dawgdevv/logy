import asyncio

from fastapi import APIRouter, HTTPException

from apps.server.schemas.entries import EntryCreate, EntryResponse, EntryUpdate
from apps.server.workers import enqueue_entry
from packages.database.repository import Repository
from packages.shared.config import settings

router = APIRouter(prefix="/api/entries", tags=["entries"])
repo = Repository(settings.db_path)


@router.get("/", response_model=list[EntryResponse])
def list_entries(limit: int = 50, offset: int = 0):
    return repo.get_entries(limit=limit, offset=offset)


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int):
    entry = repo.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.post("/", response_model=EntryResponse, status_code=201)
async def create_entry(body: EntryCreate):
    entry = repo.create_entry(
        content=body.content,
        project_name=body.project,
        category=body.category,
        difficulty=body.difficulty,
        tags=body.tags,
    )
    asyncio.create_task(enqueue_entry(entry.id))
    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: int, body: EntryUpdate):
    entry = repo.update_entry(
        entry_id=entry_id,
        content=body.content,
        category=body.category,
        difficulty=body.difficulty,
        project_name=body.project,
        tags=body.tags,
    )
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int):
    if not repo.delete_entry(entry_id):
        raise HTTPException(status_code=404, detail="Entry not found")
