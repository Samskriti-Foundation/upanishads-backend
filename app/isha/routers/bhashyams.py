from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Bhashyams"])


def get_bhashyam_or_404(sutra_id: int, language: Language, db: Session):
    db_bhashyam = (
        db.query(models.Bhashyam)
        .filter(models.Bhashyam.sutra_id == sutra_id)
        .filter(models.Bhashyam.language == language)
        .first()
    )

    if not db_bhashyam:
        not_found_error_response()

    return db_bhashyam


@router.get("/{sutra_project}/{sutra_chapter}/{sutra_no}/bhashyam", response_model=schemas.BhashyamOut)
def get_bhashyam(
    sutra_project: str, sutra_chapter: int, sutra_no: int, lang: Language = Language.en, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)

    bhashyam = get_bhashyam_or_404(sutra.id, lang, db)

    return bhashyam


@router.post("/{sutra_project}/{sutra_chapter}/{sutra_no}/bhashyam", status_code=status.HTTP_201_CREATED)
def add_bhashyam(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    bhashyam: schemas.BhashyamCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    # Retrieve sutra or raise 404 if not found
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)

    # Check if bhashyam for the given sutra and language already exists
    db_bhashyam = (
        db.query(models.Bhashyam)
        .filter(models.Bhashyam.sutra_id == sutra.id)
        .filter(models.Bhashyam.language == bhashyam.language)
        .first()
    )

    if db_bhashyam:
        conflict_error_response(
            f"Bhashyam for {sutra_project} sutra chapter {sutra_chapter} number {sutra_no} in language {bhashyam.language} already exists!"
        )

    new_bhashyam = models.Bhashyam(**bhashyam.model_dump(), sutra_id=sutra.id)

    db.add(new_bhashyam)
    db.commit()
    db.refresh(new_bhashyam)

    return {"id": new_bhashyam.id}


@router.put("/{sutra_project}/{sutra_chapter}/{sutra_no}/bhashyam", status_code=status.HTTP_204_NO_CONTENT)
def update_bhashyam(
    bhashyam: schemas.BhashyamUpdate,
    sutra_project: str='isha',
    sutra_chapter: int=0,
    sutra_no: int=0,
    lang: Language='en',
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)

    db_bhashyam = get_bhashyam_or_404(sutra.id, lang, db)

    # Update the fields
    for key, value in bhashyam.model_dump().items():
        setattr(db_bhashyam, key, value)

    db.commit()
    db.refresh(db_bhashyam)


@router.delete("/{sutra_project}/{sutra_chapter}/{sutra_no}/bhashyam", status_code=status.HTTP_204_NO_CONTENT)
def delete_bhashyam(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    lang: Language,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    bhashyam = get_bhashyam_or_404(sutra.id, lang, db)

    db.delete(bhashyam)
    db.commit()
