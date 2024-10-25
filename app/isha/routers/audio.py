from fastapi import APIRouter, Depends, File, Path, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import (
    bad_request_error_response,
    conflict_error_response,
    not_found_error_response,
)
from app.isha import models, schemas
from app.utils import Language, get_sutra_or_404

router = APIRouter(prefix="/sutras", tags=["Audio"])


def get_audio_or_404(sutra_id: int, db: Session):
    db_audio = db.query(models.Audio).filter(models.Audio.sutra_id == sutra_id).first()

    if not db_audio:
        not_found_error_response()

    return db_audio


@router.get("/{sutra_no}/audio", response_model=schemas.Audio)
def get_audio(sutra_no: int, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_no, db)

    audio = get_audio_or_404(sutra.id, db)

    return audio


@router.post("/{sutra_no}/audio")
def create_audio(
    sutra_no: int, file: UploadFile = File(None), db: Session = Depends(get_db)
):
    sutra = get_sutra_or_404(sutra_no, db)
    db_audio = db.query(models.Audio).filter(models.Audio.sutra_id == sutra.id).first()

    if db_audio:
        conflict_error_response(f"Audio for sutra {sutra_no} already exists!")

    if not file:
        bad_request_error_response("File not found")

    static_dir = Path(f"static/isha/")
    static_dir.mkdir(parents=True, exist_ok=True)
    file_extension = Path(file.filename).suffix
    file_path = static_dir / f"sutra_{sutra_no}{file_extension}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    audio = models.Audio(file_path=file, sutra_id=sutra.id)

    db.add(audio)
    db.commit()
    db.refresh(audio)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"audio": audio})


@router.put("/{sutra_no}/audio", status_code=status.HTTP_204_NO_CONTENT)
def update_audio(
    sutra_no: int,
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_audio = get_audio_or_404(sutra.id, db)

    if not file:
        bad_request_error_response("File not found")

    static_dir = Path(f"static/isha/")
    static_dir.mkdir(parents=True, exist_ok=True)
    file_extension = Path(file.filename).suffix
    file_path = static_dir / f"sutra_{sutra_no}{file_extension}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    db_audio.file_path = file_path

    db.commit()
    db.refresh(db_audio)


@router.delete("/{sutra_no}/audio", status_code=status.HTTP_204_NO_CONTENT)
def delete_audio(sutra_no: int, language: Language, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_no, db)
    audio = get_audio_or_404(sutra.id, db)

    db.delete(audio)
    db.commit()
