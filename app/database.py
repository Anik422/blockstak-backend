from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app import config

DATABASE_URL = config.DATABASE_URL

"""
Database connection and session management.
This module sets up the database engine and session for the application.
It uses SQLAlchemy to create a connection to the database specified in the configuration.
The `DATABASE_URL` is loaded from the environment variables or defaults to a SQLite database file.
"""
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    This function creates a new session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
