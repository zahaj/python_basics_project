"""
Handles all database-related operations.

This module is responsible for:
1. Establishing the connection to the PostgreSQL database using SQLAlchemy.
2. Defining the ORM models (e.g., the BriefingLog table).
3. Providing a session-maker for database interactions.
"""
import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Connection Setup ---

# These variables are provided by the environment (docker-compose.yml or ci.yml)
# This makes the database connection configurable without changing the code.
DB_USER = os.getenv("POSTGRES_USER", "briefing_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "a_secure_password")
DB_NAME = os.getenv("POSTGRES_DB", "briefing_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Model Definition ---
class BriefingLog(Base):
    """SQLAlchemy ORM model for the briefing_logs table."""
    __tablename__ = "briefing_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

def create_db_and_tables():
    """
    Creates all database tables defined in the Base metadata.

    This function is called once on application startup to ensure the
    database schema is in place.
    """
    Base.metadata.create_all(bind=engine)