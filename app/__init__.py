# Create database tables
from app.database import engine

from . import models

models.Base.metadata.create_all(bind=engine)
