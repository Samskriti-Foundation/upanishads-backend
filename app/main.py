from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.isha.main import isha
from app.routers import auth, projects, users

app = FastAPI()

origins = settings.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def health_check():
    return {"status": "available"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)

app.mount("/isha", isha)
