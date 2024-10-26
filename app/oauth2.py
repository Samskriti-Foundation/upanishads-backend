from datetime import UTC, datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import settings
from app.database import get_db

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        is_admin: bool = payload.get("is_admin")
        exp: int = payload.get("exp")

        if is_admin is None or is_admin == "":
            raise credentials_exception

        current_time = datetime.now(timezone.utc)
        token_exp_time = datetime.fromtimestamp(exp, tz=timezone.utc)

        if token_exp_time < current_time:
            raise credentials_exception

        token_data = schemas.TokenData(is_admin=is_admin, user_id=user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token Expired"
        )

    except Exception:
        raise credentials_exception

    return token_data


def set_refresh_token_cookie(response: Response, refresh_token):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        secure=True if settings.env == "production" else False,
        samesite="strict",
    )


def unset_jwt_cookie(response: Response):
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    return user


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    admin = get_current_user(token, db)

    if not admin.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin"
        )

    return admin
