from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Meanings"])
def get_meaning_or_404(sutra_id: int, language: Language, db: Session):
    db_meaning = (db.query(models.Meaning).filter(models.Meaning.sutra_id == sutra_id).filter(models.Meaning.language == language).first())
    if not db_meaning: not_found_error_response()
    return db_meaning

@router.get("/{sutra_project}/{sutra_chapter}/{sutra_no}/meaning", response_model=schemas.MeaningOut)
def get_meaning(sutra_project: str, sutra_chapter: int, sutra_no: int, lang: Language = Language.en, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    meaning = get_meaning_or_404(sutra.id, lang, db)
    return meaning
@router.post("/{sutra_project}/{sutra_chapter}/{sutra_no}/meaning", status_code=status.HTTP_201_CREATED)
def add_meaning(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    meaning: schemas.MeaningCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    # Retrieve sutra or raise 404 if not found
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)

    # Check if meaning for the given sutra and language already exists
    db_meaning = (db.query(models.Meaning).filter(models.Meaning.sutra_id == sutra.id).filter(models.Meaning.language == meaning.language).first())
    if db_meaning: conflict_error_response(f"Meaning for {sutra_project} sutra chapter {sutra_chapter} number {sutra_no} in language {meaning.language} already exists!")
    new_meaning = models.Meaning(**meaning.model_dump(), sutra_id=sutra.id)
    db.add(new_meaning)
    db.commit()
    db.refresh(new_meaning)
    return {"id": new_meaning.id}

@router.put("/{sutra_project}/{sutra_chapter}/{sutra_no}/meaning", status_code=status.HTTP_204_NO_CONTENT)
def update_meaning(
    meaning: schemas.MeaningUpdate,
    sutra_project: str='isha',
    sutra_chapter: int=0,
    sutra_no: int=0,
    lang: Language='en',
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    db_meaning = get_meaning_or_404(sutra.id, lang, db)
    if db_meaning:
        # Update the fields
        for key, value in meaning.model_dump().items(): setattr(db_meaning, key, value)
        db.commit()
        db.refresh(db_meaning)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f'Updated sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no} text "{meaning.model_dump()["text"]}"')
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} meaning {meaning.model_dump()["language"]} not found")

@router.delete("/{sutra_project}/{sutra_chapter}/{sutra_no}/meaning", status_code=status.HTTP_204_NO_CONTENT)
def delete_meaning(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    lang: Language,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    meaning = get_meaning_or_404(sutra.id, lang, db)
    if meaning:
        db.delete(meaning)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Deleted sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no} meaning")
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} meaning not found")
