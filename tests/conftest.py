import pytest
import os

from daily_briefing.database import engine, Base

# Ensure DB env vars are set with sensible defaults
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "briefing_user")
os.environ.setdefault("DB_PASSWORD", "a_secure_password")
os.environ.setdefault("DB_NAME", "briefing_db_test")  # local fallback

print(f"[conftest] Using DB_HOST={os.environ['DB_HOST']} DB_NAME={os.environ['DB_NAME']}")

@pytest.fixture(scope="session")
def db_session_setup():
    """
    A session-scoped fixture to set up the database once for all tests
    that need it.
    """

    # Drop all tables to ensure a clean state
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield # The tests run here