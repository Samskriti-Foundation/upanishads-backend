from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2
from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language, Philosophy

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Interpretations"])


def get_interpretation_or_404(sutra_id: int, language: Language, phil: Philosophy, db: Session):
    db_interpretation = (
        db.query(models.Interpretation)
        .filter(models.Interpretation.sutra_id == sutra_id)
        .filter(models.Interpretation.language == language)
        .filter(models.Interpretation.philosophy == phil)
        .first()
    )
    if not db_interpretation:not_found_error_response()
    return db_interpretation

@router.get("/{sutra_project}/{sutra_chapter}/{sutra_no}/interpretation", response_model=schemas.InterpretationOut)
def get_interpretation(sutra_project: str, sutra_chapter: int, sutra_no: int, lang: Language = Language.en, phil: Philosophy = Philosophy.advaita, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    interpretation = get_interpretation_or_404(sutra.id, lang, phil, db)
    return interpretation

@router.post("/{sutra_project}/{sutra_chapter}/{sutra_no}/interpretation", status_code=status.HTTP_201_CREATED)
def add_interpretation(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    interpretation: schemas.InterpretationCreate,
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    # Retrieve sutra or raise 404 if not found
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    # Check if interpretation for the given sutra and language already exists
    db_interpretation = (
        db.query(models.Interpretation)
        .filter(models.Interpretation.sutra_id == sutra.id)
        .filter(models.Interpretation.language == interpretation.language)
        .filter(models.Interpretation.philosophy == interpretation.philosophy)
        .first()
    )
    if db_interpretation:conflict_error_response(f"Interpretation for {sutra_project} sutra chapter {sutra_chapter} number {sutra_no} in language {interpretation.language} philosophy {interpretation.philosophy} already exists!")
    new_interpretation = models.Interpretation(**interpretation.model_dump(), sutra_id=sutra.id)
    db.add(new_interpretation)
    db.commit()
    db.refresh(new_interpretation)
    return {"id": new_interpretation.id}

@router.put("/{sutra_project}/{sutra_chapter}/{sutra_no}/interpretation", status_code=status.HTTP_204_NO_CONTENT)
def update_interpretation(
    interpretation: schemas.InterpretationUpdate,
    sutra_project: str='kena',
    sutra_chapter: int=0,
    sutra_no: int=0,
    lang: Language='en',
    phil: Philosophy="adv",
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    db_interpretation = get_interpretation_or_404(sutra.id, lang, phil, db)
    if db_interpretation:
        # Update the fields
        for key, value in interpretation.model_dump().items(): setattr(db_interpretation, key, value)
        db.commit()
        db.refresh(db_interpretation)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=f'Updated sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no} text "{interpretation.model_dump()["text"]}"')
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} interpretation {interpretation.model_dump()["language"]} not found")

@router.delete("/{sutra_project}/{sutra_chapter}/{sutra_no}/interpretation", status_code=status.HTTP_204_NO_CONTENT)
def delete_interpretation(
    sutra_project: str,
    sutra_chapter: int,
    sutra_no: int,
    lang: Language,
    phil: Philosophy,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_project, sutra_chapter, sutra_no, db)
    interpretation = get_interpretation_or_404(sutra.id, lang, phil, db)
    if interpretation:
        db.delete(interpretation)
        db.commit()
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Deleted sutra {sutra_project} chapter {sutra_chapter} sutra {sutra_no} interpretation")
    else: raise HTTPException(status_code=404, detail=f"Project {sutra_project} chapter {sutra_chapter} sutra {sutra_no} interpretation not found")

