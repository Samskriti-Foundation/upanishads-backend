from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models as app_models
from app import oauth2, utils
from app.database import get_db
from app.errors import conflict_error_response, not_found_error_response
from app.isha import models, schemas

from .utils import get_sutra_or_404

STATIC_AUDIO_DIR = Path("static/isha/")
STATIC_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/sutras", tags=["Audio"])


def get_audio_or_404(sutra_id: int, mode: utils.Mode, db: Session):
    db_audio = (
        db.query(models.Audio)
        .filter(models.Audio.sutra_id == sutra_id, models.Audio.mode == mode)
        .first()
    )

    if not db_audio:
        return not_found_error_response()

    return db_audio


@router.get("/{sutra_no}/audio", response_model=schemas.Audio)
def get_audio(sutra_no: int, mode: utils.Mode, db: Session = Depends(get_db)):
    sutra = get_sutra_or_404(sutra_no, db)
    audio = get_audio_or_404(sutra.id, mode, db)
    return audio


@router.post("/{sutra_no}/audio", status_code=status.HTTP_201_CREATED)
def create_audio(
    sutra_no: int,
    mode: utils.Mode,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_no, db)

    db_audio = (
        db.query(models.Audio)
        .filter(models.Audio.sutra_id == sutra.id, models.Audio.mode == mode)
        .first()
    )

    if db_audio:
        return conflict_error_response(
            f"Audio for sutra {sutra_no} in {mode} mode already exists!"
        )

    mode_dir = STATIC_AUDIO_DIR / mode
    mode_dir.mkdir(parents=True, exist_ok=True)
    file_extension = Path(file.filename or "").suffix
    file_path = mode_dir / f"sutra_{sutra_no}{file_extension}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    audio = models.Audio(file_path=str(file_path), sutra_id=sutra.id, mode=mode)
    db.add(audio)
    db.commit()
    db.refresh(audio)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"audio": {"id": audio.id, "file_path": audio.file_path}},
    )


@router.put("/{sutra_no}/audio", status_code=status.HTTP_204_NO_CONTENT)
def update_audio(
    sutra_no: int,
    mode: utils.Mode,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: app_models.User = Depends(oauth2.get_current_user),
):
    sutra = get_sutra_or_404(sutra_no, db)
    db_audio = get_audio_or_404(sutra.id, mode, db)

    mode_dir = STATIC_AUDIO_DIR / mode
    mode_dir.mkdir(parents=True, exist_ok=True)
    file_extension = Path(file.filename or "").suffix
    file_path = mode_dir / f"sutra_{sutra_no}{file_extension}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    db_audio.file_path = str(file_path)
    db.commit()
    db.refresh(db_audio)


@router.delete("/{sutra_no}/audio", status_code=status.HTTP_204_NO_CONTENT)
def delete_audio(
    sutra_no: int,
    mode: utils.Mode,
    db: Session = Depends(get_db),
    current_admin: app_models.User = Depends(oauth2.get_current_admin),
):
    sutra = get_sutra_or_404(sutra_no, db)
    audio = get_audio_or_404(sutra.id, mode, db)

    db.delete(audio)
    db.commit()
