from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Meanings"])


def get_meaning_or_404(sutra_id: int, language: Language, db: Session):
    db_meaning = (
        db.query(models.Meaning)
        .filter(models.Meaning.sutra_id == sutra_id)
        .filter(models.Meaning.language == language)
        .first()
    )

    if not db_meaning:
        not_found_error_response()


@router.get("/{sutra_no}/meaning", response_model=schemas.MeaningOut)
def get_meaning(
    sutra_no: int, lang: Language = Language.en, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)

    meaning = get_meaning_or_404(sutra.id, lang, db)

    return meaning


@router.post("/{sutra_no}/meaning")
def create_meaning(
    sutra_no: int, meaning: schemas.MeaningCreate, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_meaning = get_meaning_or_404(sutra.id, meaning.language, db)

    if db_meaning:
        conflict_error_response(f"Meaning for sutra {sutra_no} already exists!")

    meaning = models.Meaning(**meaning.model_dump())

    db.add(meaning)
    db.commit()
    db.refresh(meaning)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"meaning": meaning}
    )


@router.put("/{sutra_no}/meaning", status_code=status.HTTP_204_NO_CONTENT)
def update_meaning(
    sutra_no: int,
    lang: Language,
    meaning: schemas.MeaningUpdate,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_meaning = get_meaning_or_404(sutra.id, lang, db)

    # Update the fields
    for key, value in meaning.model_dump().items():
        setattr(db_meaning, key, value)

    db.commit()
    db.refresh(db_meaning)


@router.delete("/{sutra_no}/meaning", status_code=status.HTTP_204_NO_CONTENT)
def delete_meaning(sutra_no: int, language: Language, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_no, db)
    meaning = get_meaning_or_404(sutra.id, language, db)

    db.delete(meaning)
    db.commit()
