from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response
from app.isha import models, schemas

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Sutras"])


@router.get("/", response_model=List[schemas.SutraListOut])
def get_sutras(db: Session = Depends(get_db)):
    return db.query(models.Sutra.id, models.Sutra.number).all()


@router.get("/{sutra_no}", response_model=schemas.SutraOut)
def get_sutra(sutra_no: int, db: Session = Depends(get_db)):
    return get_sutra_or_404(sutra_no, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_sutra(
    sutra: schemas.SutraCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra_db = (
        db.query(models.Sutra).filter(models.Sutra.number == sutra.number).first()
    )

    if sutra_db:
        conflict_error_response(f"Sutra with number {sutra.number} already exists!")

    sutra = models.Sutra(**sutra.model_dump())

    db.add(sutra)
    db.commit()
    db.refresh(sutra)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"id": sutra.id},
    )


@router.put("/{sutra_no}", status_code=status.HTTP_204_NO_CONTENT)
def update_sutra(
    sutra_no: int,
    sutra_update: schemas.SutraUpdate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_no, db)

    for key, value in sutra_update.model_dump().items():
        setattr(sutra, key, value)

    db.commit()


@router.delete("/{sutra_no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sutra(
    sutra_no: int,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db.delete(sutra)
    db.commit()
