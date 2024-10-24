from fastapi import FastAPI

from .routers import interpretations, meanings, sutras, transliterations

isha = FastAPI(title="Ishavasyopanishad")

isha.include_router(sutras.router)
isha.include_router(meanings.router)
isha.include_router(transliterations.router)
isha.include_router(interpretations.router)
