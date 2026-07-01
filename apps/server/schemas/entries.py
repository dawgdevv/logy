from datetime import datetime

from pydantic import BaseModel

from apps.server.schemas.projects import ProjectResponse
from packages.shared.constants import Difficulty


class EntryBase(BaseModel):
    content: str
    category: str = "other"
    difficulty: Difficulty = Difficulty.medium


class EntryCreate(EntryBase):
    project: str | None = None
    tags: list[str] | None = None


class EntryUpdate(BaseModel):
    content: str | None = None
    category: str | None = None
    difficulty: Difficulty | None = None
    project: str | None = None
    tags: list[str] | None = None


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class EntryResponse(EntryBase):
    id: int
    project_id: int | None
    created_at: datetime
    updated_at: datetime
    project: ProjectResponse | None = None
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}
