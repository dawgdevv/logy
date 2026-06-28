from fastapi import APIRouter, HTTPException

from apps.server.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate
from packages.database.repository import Repository
from packages.shared.config import settings

router = APIRouter(prefix="/api/projects", tags=["projects"])
repo = Repository(settings.db_path)


@router.get("/", response_model=list[ProjectResponse])
def list_projects():
    return repo.get_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    project = repo.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(body: ProjectCreate):
    return repo.create_project(name=body.name, description=body.description)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, body: ProjectUpdate):
    project = repo.update_project(
        project_id=project_id,
        name=body.name,
        description=body.description,
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int):
    if not repo.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
