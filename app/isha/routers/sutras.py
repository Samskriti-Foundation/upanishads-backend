from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.isha import models, schemas
from app.isha.database import get_db

router = APIRouter(prefix="/sutras", tags=["Sutras"])


def get_sutra_or_404(sutra_no: int, db: Session):
    sutra = db.query(models.Sutra).filter(models.Sutra.number == sutra_no).first()

    if not sutra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sutra with number {sutra_no} not found",
        )

    return sutra


@router.get("/", response_model=List[schemas.SutraOut])
def get_sutras(db: Session = Depends(get_db)):
    return db.query(models.Sutra).all()


@router.get("/{sutra_no}", response_model=schemas.SutraOut)
def get_sutra(sutra_no: int, db: Session = Depends(get_db)):
    return get_sutra_or_404(sutra_no, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_sutra(sutra: schemas.SutraCreate, db: Session = Depends(get_db)):
    sutra_db = (
        db.query(models.Sutra).filter(models.Sutra.number == sutra.number).first()
    )

    if sutra_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": f"Sutra with number {sutra.number} already exists!"},
        )

    sutra = models.Sutra(**sutra.model_dump())

    db.add(sutra)
    db.commit()
    db.refresh(sutra)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": f"Created sutra with number {sutra.number}"},
    )


@router.put("/{sutra_no}", response_model=schemas.SutraOut)
def update_sutra(
    sutra_no: int, sutra_update: schemas.SutraUpdate, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)

    for key, value in sutra_update.model_dump().items():
        setattr(sutra, key, value)

    db.commit()
    db.refresh(sutra)

    return sutra


@router.delete("/{sutra_no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sutra(sutra_no: int, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_no, db)

    db.delete(sutra)
    db.commit()
