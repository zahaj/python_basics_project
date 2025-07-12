import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Database Connection Setup ---

# Construct the database URL from environment variables.
DB_USER = os.getenv("POSTGRES_USER", "briefing_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "a_secure_password")
DB_NAME = os.getenv("POSTGRES_DB", "briefing_db")
DB_HOST = "db"
DB_PORT = "5432"

# The standard database URL format is postgresql://user:password@host/dbname.
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Add this below the DATABASE_URL

# The 'engine' is the core interface to the database.
engine = create_engine(DATABASE_URL)

# The 'SessionLocal' class will be our factory for creating database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' is the factory for our declarative model classes.
Base = declarative_base()

# --- SQLAlchemy Model Definition ---

class BriefingLog(Base):
    """SQLAlchemy model for the briefing_logs table."""
    __tablename__ = "briefing_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

def create_db_and_tables():
    """
    Creates all database tables defined by classes inheriting from Base.
    This is typically called once on application startup.
    """
    Base.metadata.create_all(bind=engine)