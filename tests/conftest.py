import pytest
import os

from daily_briefing.database import engine, Base

if "DB_HOST" not in os.environ:
    if os.getenv("CI"):  # GitHub Actions sets CI=true
        os.environ["DB_HOST"] = "postgres"
    else:
        os.environ["DB_HOST"] = "localhost"

print(f"[conftest] Using DB_HOST={os.environ['DB_HOST']}")

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