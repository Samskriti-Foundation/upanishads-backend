from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.isha import models
from app.isha.database import get_db

router = APIRouter(prefix="/sutras", tags=["Sutras"])


@router.get("/")
def get_sutras(db: Session = Depends(get_db)):
    return db.query(models.Sutra).all()


@router.get("/{sutra_no}")
def get_sutra(sutra_no: int, db: Session = Depends(get_db)):
    sutra = db.query(models.Sutra).filter(models.Sutra.number == sutra_no).first()

    if not sutra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sutra with number {sutra_no} not found",
        )

    return sutra


@router.post("/")
def add_sutra(db: Session = Depends(get_db)):
    return ""
