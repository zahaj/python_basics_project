import pytest
import os

# This line MUST run before any of your application's
# modules are imported, especially 'database.py'.
if os.getenv("CI"):  # GitHub sets this automatically in Actions
    os.environ["DB_HOST"] = "postgres"
else:
    os.environ.setdefault("DB_HOST", "localhost")

from daily_briefing.database import engine, Base

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