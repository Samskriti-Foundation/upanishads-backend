from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.isha import models, schemas


router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/{term}", response_model=List[schemas.Result])
def search(term: str, db: Session = Depends(get_db)):
    results = []

    sutras = db.query(models.Sutra).filter(models.Sutra.text.ilike(f"%{term}%")).all()
    for sutra in sutras:
        results.append({
            "text": sutra.text,
            "sutra_no": sutra.number,
            "mode": "chant",
            "lang": None
        })

    meanings = db.query(models.Meaning).filter(models.Meaning.text.ilike(f"%{term}%")).all()
    for meaning in meanings:
        results.append({
            "text": meaning.text,
            "sutra_no": meaning.sutra.number,
            "mode": "chant",
            "lang": meaning.language
        })


    transliterations = db.query(models.Transliteration).filter(models.Transliteration.text.ilike(f"%{term}%")).all()
    for transliteration in transliterations:
        results.append({
            "text": transliteration.text,
            "sutra_no": transliteration.sutra.number,
            "mode": "chant",
            "lang": transliteration.language
        })

    interpretations = db.query(models.Interpretation).filter(models.Interpretation.text.ilike(f"%{term}%")).all()
    for interpretation in interpretations:
        results.append({
            "text": interpretation.text,
            "sutra_no": interpretation.sutra.number,
            "mode": f"interpretation - {interpretation.philosophy}",
            "lang": interpretation.language
        })

    return results
