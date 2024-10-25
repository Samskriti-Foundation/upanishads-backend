from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# Retrieve the database URL from the settings
SQLALCHEMY_DATABASE_URL = settings.db_url

# Create an SQLAlchemy engine instance
# The engine is responsible for connecting to the database and managing the connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
# SessionLocal will be a factory for new Session objects
# autocommit=False ensures that transactions are managed manually
# autoflush=False prevents automatic flushing of the session (committing changes to the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our declarative models to inherit from
# This will allow SQLAlchemy to keep track of our models and their mappings to the database tables
Base = declarative_base()


# Dependency to get a session object
# This function provides a database session that can be used in API endpoints
# It ensures that the session is closed after the request is completed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
