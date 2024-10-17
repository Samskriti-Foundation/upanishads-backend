from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.isha.database import get_db

from .utils import Language, get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Transliterations"])


def get_transliteration_or_404(sutra_id: int, language: Language, db: Session):
    db_transliteration = (
        db.query(models.Transliteration)
        .filter(models.Transliteration.sutra_id == sutra_id)
        .filter(models.Transliteration.language == language)
        .first()
    )

    if not db_transliteration:
        not_found_error_response()


@router.get("/{sutra_no}/transliteration", response_model=schemas.TransliterationOut)
def get_transliteration(
    sutra_no: int, lang: Language = Language.en, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)

    transliteration = get_transliteration_or_404(sutra.id, lang, db)

    return transliteration


@router.post("/{sutra_no}/transliteration")
def create_transliteration(
    sutra_no: int,
    transliteration: schemas.TransliterationCreate,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_transliteration = get_transliteration_or_404(
        sutra.id, transliteration.language, db
    )

    if db_transliteration:
        conflict_error_response(f"Transliteration for sutra {sutra_no} already exists!")

    transliteration = models.Transliteration(**transliteration.model_dump())

    db.add(transliteration)
    db.commit()
    db.refresh(transliteration)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"transliteration": transliteration},
    )


@router.put("/{sutra_no}/transliteration", status_code=status.HTTP_204_NO_CONTENT)
def update_transliteration(
    sutra_no: int,
    lang: Language,
    transliteration: schemas.TransliterationUpdate,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_transliteration = get_transliteration_or_404(sutra.id, lang, db)

    # Update the fields
    for key, value in transliteration.model_dump().items():
        setattr(db_transliteration, key, value)

    db.commit()
    db.refresh(db_transliteration)


@router.delete("/{sutra_no}/transliteration", status_code=status.HTTP_204_NO_CONTENT)
def delete_transliteration(
    sutra_no: int, language: Language, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)
    transliteration = get_transliteration_or_404(sutra.id, language, db)

    db.delete(transliteration)
    db.commit()
