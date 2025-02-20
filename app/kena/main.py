from fastapi import FastAPI
from app.config import settings
from .routers import audio, interpretations, meanings, sutras, transliterations, search, bhashyams

kena = FastAPI(
    title="Kenopanishad",
    docs_url=None if settings.env == "production" else "/docs",
    redoc_url=None if settings.env == "production" else "/redoc",
)
@kena.get("/healthz")
def health_check():
    return {"status": "kena - available", "environment": settings.env}

kena.include_router(sutras.router)
kena.include_router(meanings.router)
kena.include_router(transliterations.router)
kena.include_router(interpretations.router)
kena.include_router(bhashyams.router)
kena.include_router(audio.router)
kena.include_router(search.router)
