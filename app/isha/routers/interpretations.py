from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas
from app.utils import Language, Philosophy

from .utils import get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Interpretations"])


def get_interpretation_or_404(
    sutra_id: int, language: Language, philosophy_type: Philosophy, db: Session
):
    db_interpretation = (
        db.query(models.Interpretation)
        .filter(models.Interpretation.sutra_id == sutra_id)
        .filter(models.Interpretation.language == language)
        .filter(models.Interpretation.philosophy_type == philosophy_type)
        .first()
    )

    if not db_interpretation:
        not_found_error_response()


@router.get("/{sutra_no}/interpretation", response_model=schemas.InterpretationOut)
def get_interpretation(
    sutra_no: int,
    lang: Language = Language.en,
    ptype: Philosophy = Philosophy.advaita,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    interpretation = get_interpretation_or_404(sutra.id, lang, ptype, db)

    return interpretation


@router.post("/{sutra_no}/interpretation")
def create_interpretation(
    sutra_no: int,
    interpretation: schemas.InterpretationCreate,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_interpretation = get_interpretation_or_404(
        sutra.id, interpretation.language, interpretation.philosophy_type, db
    )

    if db_interpretation:
        conflict_error_response(f"Interpretation for sutra {sutra_no} already exists!")

    interpretation = models.Interpretation(**interpretation.model_dump())

    db.add(interpretation)
    db.commit()
    db.refresh(interpretation)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"interpretation": interpretation},
    )


@router.put("/{sutra_no}/interpretation", status_code=status.HTTP_204_NO_CONTENT)
def update_interpretation(
    sutra_no: int,
    lang: Language,
    interpretation: schemas.InterpretationUpdate,
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_interpretation = get_interpretation_or_404(
        sutra.id, lang, interpretation.philosophy_type, db
    )

    # Update the fields
    for key, value in interpretation.model_dump().items():
        setattr(db_interpretation, key, value)

    db.commit()
    db.refresh(db_interpretation)


@router.delete("/{sutra_no}/interpretation", status_code=status.HTTP_204_NO_CONTENT)
def delete_interpretation(
    sutra_no: int, language: Language, ptype: Philosophy, db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)
    interpretation = get_interpretation_or_404(sutra.id, language, ptype, db)

    db.delete(interpretation)
    db.commit()
