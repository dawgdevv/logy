from pathlib import Path

from sqlalchemy import Engine
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, create_engine, select

from packages.database.models import Entry, EntryTagLink, Project, Tag
from packages.shared.constants import Difficulty


def get_engine(db_path: Path) -> Engine:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine


class Repository:
    def __init__(self, db_path: Path) -> None:
        self.engine = get_engine(db_path)

    def _session(self) -> Session:
        return Session(self.engine)

    def create_entry(
        self,
        content: str,
        project_name: str | None = None,
        category: str = "other",
        difficulty: Difficulty = Difficulty.medium,
        tags: list[str] | None = None,
    ) -> Entry:
        with self._session() as session:
            project = None
            if project_name:
                result = session.exec(select(Project).where(Project.name == project_name))
                project = result.first()
                if not project:
                    project = Project(name=project_name)
                    session.add(project)
                    session.flush()

            entry = Entry(
                content=content,
                project_id=project.id if project else None,
                category=category,
                difficulty=difficulty,
            )
            session.add(entry)
            session.flush()

            if tags:
                for tag_name in tags:
                    result = session.exec(select(Tag).where(Tag.name == tag_name))
                    tag = result.first()
                    if not tag:
                        tag = Tag(name=tag_name)
                        session.add(tag)
                        session.flush()
                    link = EntryTagLink(entry_id=entry.id, tag_id=tag.id)
                    session.add(link)

            session.commit()
            session.refresh(entry)
            return entry

    def get_entries(self, limit: int = 50, offset: int = 0) -> list[Entry]:
        with self._session() as session:
            statement = (
                select(Entry)
                .options(selectinload(Entry.project), selectinload(Entry.tags))
                .order_by(Entry.created_at.desc())
                .offset(offset)
                .limit(limit)
            )
            return list(session.exec(statement).all())

    def get_entry(self, entry_id: int) -> Entry | None:
        with self._session() as session:
            statement = (
                select(Entry)
                .options(selectinload(Entry.project), selectinload(Entry.tags))
                .where(Entry.id == entry_id)
            )
            return session.exec(statement).first()

    def get_projects(self) -> list[Project]:
        with self._session() as session:
            statement = (
                select(Project)
                .options(selectinload(Project.entries))
                .order_by(Project.updated_at.desc())
            )
            return list(session.exec(statement).all())

    def get_project(self, project_id: int) -> Project | None:
        with self._session() as session:
            statement = (
                select(Project)
                .options(selectinload(Project.entries))
                .where(Project.id == project_id)
            )
            return session.exec(statement).first()

    def get_project_by_name(self, name: str) -> Project | None:
        with self._session() as session:
            statement = (
                select(Project).options(selectinload(Project.entries)).where(Project.name == name)
            )
            return session.exec(statement).first()

    def search_entries(self, query: str) -> list[Entry]:
        with self._session() as session:
            statement = (
                select(Entry)
                .options(selectinload(Entry.project), selectinload(Entry.tags))
                .where(Entry.content.contains(query))
            )
            return list(session.exec(statement).all())
