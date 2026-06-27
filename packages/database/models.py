from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from packages.shared.constants import Difficulty
from packages.shared.utils import utcnow


class EntryTagLink(SQLModel, table=True):
    __tablename__ = "entry_tags"
    entry_id: int | None = Field(
        default=None, foreign_key="entries.id", primary_key=True
    )
    tag_id: int | None = Field(
        default=None, foreign_key="tags.id", primary_key=True
    )


class Entry(SQLModel, table=True):
    __tablename__ = "entries"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    project_id: int | None = Field(default=None, foreign_key="projects.id")
    category: str = Field(default="other")
    difficulty: Difficulty = Field(default=Difficulty.medium)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    project: Optional["Project"] = Relationship(back_populates="entries")
    tags: list["Tag"] = Relationship(back_populates="entries", link_model=EntryTagLink)


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str = Field(default="")
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)

    entries: list[Entry] = Relationship(back_populates="project")


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    entries: list[Entry] = Relationship(back_populates="tags", link_model=EntryTagLink)
