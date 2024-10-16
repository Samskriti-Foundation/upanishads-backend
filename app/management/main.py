from fastapi import FastAPI

from .routers import auth, projects, users

management = FastAPI(title="Upanishads - Admin Management")

management.include_router(auth.router)
management.include_router(users.router)
management.include_router(projects.router)
