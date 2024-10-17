from enum import Enum

from sqlalchemy.orm import Session

from app.errors import not_found_error_response
from app.isha import models


def get_sutra_or_404(sutra_no: int, db: Session) -> models.Sutra:
    sutra = db.query(models.Sutra).filter(models.Sutra.number == sutra_no).first()

    if not sutra:
        not_found_error_response()

    return sutra


class Language(str, Enum):
    en = "en"  # English
    kn = "kn"  # Kannada
    ta = "ta"  # Tamil
    te = "te"  # Telugu
    hi = "hi"  # Hindi
