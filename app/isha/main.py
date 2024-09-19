from fastapi import FastAPI

from .routers import sutras

isha = FastAPI(title="Ishavasyopanishad")

isha.include_router(sutras.router)
