from fastapi import APIRouter, HTTPException

from packages.database.repository import Repository
from packages.shared.config import settings

router = APIRouter(prefix="/projects", tags=["projects"])
repo = Repository(settings.db_path)


@router.get("/")
def list_projects():
    return repo.get_projects()


@router.get("/{project_id}")
def get_project(project_id: int):
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
