from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils
from app.database import get_db
from app.oauth2 import get_current_admin, get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_or_404(project_id: int, db: Session):
    project = (
        db.query(models.Project).filter(models.Project.number == project_id).first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found",
        )

    return project


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = get_project_or_404(project_id, db)
    return project


@router.post("/")
def add_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project_db = (
        db.query(models.Project).filter(models.Project.name == project.name).first()
    )

    if project_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Project with name {project.name} already exists",
        )

    db.add(project)
    db.commit()
    db.refresh(project)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=f"Created project with ID {project.id}",
    )


@router.put("/{project_id}")
def update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin),
):
    project = get_project_or_404(project_id, db)
