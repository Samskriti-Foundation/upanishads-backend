from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.errors import not_found_error_response
from app.isha import models
from app import models as app_models


def get_sutra_or_404(sutra_project: str, sutra_chapter: int, sutra_no: int, db: Session) -> models.Sutra:
    project = db.query(app_models.Project).filter(app_models.Project.name == sutra_project).first()
    if not project: not_found_error_response()
    sutra = db.query(models.Sutra).filter(and_(models.Sutra.project_id == project.id, models.Sutra.chapter == sutra_chapter, models.Sutra.number == sutra_no)).first()
    if not sutra: not_found_error_response()
    return sutra
