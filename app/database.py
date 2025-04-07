from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Database connection URL from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create an engine to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is the session factory that provides a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all model classes to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session.
    Ensures that a session is correctly closed after use.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to the route handler
    finally:
        db.close()  # Ensure the session is closed after use
