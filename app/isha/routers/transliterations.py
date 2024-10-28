from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language

from .utils import get_sutra_or_404

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

    return db_transliteration


@router.get("/{sutra_no}/transliteration", response_model=schemas.TransliterationOut)
def get_transliteration(
    sutra_no: int, lang: Language = Language.en, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)

    transliteration = get_transliteration_or_404(sutra.id, lang, db)

    return transliteration


@router.post("/{sutra_no}/transliteration", status_code=status.HTTP_201_CREATED)
def add_transliteration(
    sutra_no: int,
    transliteration: schemas.TransliterationCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    # Retrieve sutra or raise 404 if not found
    sutra = get_sutra_or_404(sutra_no, db)

    # Check if transliteration for the given sutra and language already exists
    db_transliteration = (
        db.query(models.Transliteration)
        .filter(models.Transliteration.sutra_id == sutra.id)
        .filter(models.Transliteration.language == transliteration.language)
        .first()
    )

    if db_transliteration:
        conflict_error_response(
            f"Transliteration for sutra {sutra_no} in language {transliteration.language} already exists!"
        )

    new_transliteration = models.Transliteration(
        **transliteration.model_dump(), sutra_id=sutra.id
    )

    db.add(new_transliteration)
    db.commit()
    db.refresh(new_transliteration)

    return {"id": new_transliteration.id}


@router.put("/{sutra_no}/transliteration", status_code=status.HTTP_204_NO_CONTENT)
def update_transliteration(
    sutra_no: int,
    lang: Language,
    transliteration: schemas.TransliterationUpdate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
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
    sutra_no: int,
    lang: Language,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_no, db)
    transliteration = get_transliteration_or_404(sutra.id, lang, db)

    db.delete(transliteration)
    db.commit()
