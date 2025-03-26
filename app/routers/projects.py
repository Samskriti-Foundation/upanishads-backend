from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils
from app.database import get_db
from app.oauth2 import get_current_admin, get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_by_id_or_404(project_id: str, db: Session):
    project = (db.query(models.Project).filter(models.Project.id == project_id).first())
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project ID {project_id} not found",
        )
    return project

def get_project_or_404(project_name: str, db: Session):
    project = (db.query(models.Project).filter(models.Project.name == project_name).first())

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_name} not found",
        )

    return project


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects


@router.get("_by_id/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = get_project_by_id_or_404(project_id, db)
    return project

@router.get("_by_name/{project_name}")
def get_project_by_name(project_name: str, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.name == project_name).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_name} not found",
        )
    return project

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_project(
    project: schemas.ProjectCreate,
    name : str, description: str,
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

    db_project = models.Project(name=name, description=description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    # return db_project
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=f"Created project {project.name}")

@router.put("/{project_id}")
def update_project(
    project_id: int,
    project: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin),
):
    project = get_project_or_404(project_id, db)

@router.delete("_by_name/{project_name}")
def delete_project(
    project_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    project = db.query(models.Project).filter(models.Project.name == project_name).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_name} not found",
        )
    db.delete(project)
    db.commit()
    return JSONResponse(f"Project {project_name} removed")

@router.delete("_by_id/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    db.delete(project)
    db.commit()
    return JSONResponse(f"Project {project_id} {project.name} removed")

