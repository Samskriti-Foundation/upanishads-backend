from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response
from app.isha import models, schemas
from app import models as app_models, schemas as app_schemas
from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Sutras"])

def get_sutra_by_id_or_404(sutra_id: int, db: Session):
    sutra = (db.query(models.Sutra).filter(models.Sutra.id == sutra_id).first())
    if not sutra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sutra ID {sutra_id} not found",
        )
    return sutra
@router.get("/total-count", response_model=int)
def get_sutras_count(project_name: str = "kena", db: Session = Depends(get_db)):
    db_project = db.query(app_models.Project).filter(app_models.Project.name == project_name).first()
    if db_project is None: raise HTTPException(status_code=404, detail=f"Project {project_name} not found")
    sutras_count = db.query(models.Sutra.project_id, models.Sutra.id, models.Sutra.number).filter(models.Sutra.project_id == db_project.id).count()
    return sutras_count

@router.get("/", response_model=List[schemas.SutraListOut])
def get_sutras(project_name: str = "kena", db: Session = Depends(get_db)):
    db_project = db.query(app_models.Project).filter(app_models.Project.name == project_name).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail=f"Project {project_name} not found")
    sutras = db.query(models.Sutra.project_id, models.Sutra.id, models.Sutra.number).filter(models.Sutra.project_id == db_project.id).all()
    return sutras
    # return db.query(models.Sutra.id, models.Sutra.number).all()


@router.get("/{sutra_project}/{sutra_chapter}/{sutra_no}", response_model=schemas.SutraOut)
def get_sutra(sutra_project: str='isha', sutra_chapter: int=0, sutra_no: int=0, db: Session = Depends(get_db)):
    return get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
@router.get("_by_id/{sutra_id}")
def get_project(sutra_id: int, db: Session = Depends(get_db)):
    sutra = get_sutra_by_id_or_404(sutra_id, db)
    return sutra
@router.post("/", status_code=status.HTTP_201_CREATED)

def add_sutra(
    project: app_schemas.ProjectCreate,
    sutra: schemas.SutraCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    db_project = db.query(app_models.Project).filter(app_models.Project.name == project.name).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail=f"Project {project.name} not found")

    sutra_db = (
        db.query(models.Sutra).filter(and_(models.Sutra.project_id == db_project.id, models.Sutra.chapter == sutra.chapter, models.Sutra.number == sutra.number)).first()
    )

    if sutra_db:
        conflict_error_response(f"{project.name} Sutra - chapter {sutra.chapter}, number {sutra.number} already exists!")

    sutra = models.Sutra(
        chapter=sutra.chapter,
        number=sutra.number,
        text=sutra.text,
        project_id=db_project.id
    )
    db.add(sutra)
    db.commit()
    db.refresh(sutra)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": sutra.id},
    )

@router.put("/{sutra_project}/{sutra_chapter}/{sutra_no}", status_code=status.HTTP_202_ACCEPTED)
# @router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def update_sutra(
    sutra_update: schemas.SutraUpdate,
    sutra_project: str='isha',
    sutra_chapter: int=0,
    sutra_no: int=0,
    # sutra_text: str="?",
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    if sutra:
        sutra_update_items = sutra_update.model_dump()
        sutra_text = sutra_update_items["text"]
        for key, value in sutra_update_items.items():
            setattr(sutra, key, value)
        db.commit()
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f"Updated sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no} text {sutra_text}")
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} not found")

@router.delete("/{sutra_project}/{sutra_chapter}/{sutra_no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sutra(
    sutra_project: str='isha',
    sutra_chapter: int=0,
    sutra_no: int=0,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    if sutra:
        db.delete(sutra)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Deleted sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no}")
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} not found")
@router.delete("_by_id/{sutra_id}")
def delete_sutra_by_id(sutra_id: int, db: Session = Depends(get_db)):
    sutra = get_sutra_by_id_or_404(sutra_id, db)
    if sutra:
        db.delete(sutra)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Deleted sutra {sutra_id}")
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_id}not found")
