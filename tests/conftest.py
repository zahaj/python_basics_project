import pytest
import os

# This line MUST run before any of your application's
# modules are imported, especially 'database.py'.
os.environ['DB_HOST'] = 'localhost'

from daily_briefing.database import engine, Base, SessionLocal

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    A session-scoped fixture to set up the database once for all tests.
    The 'autouse=True' means this fixture will be automatically used for
    every test, so you don't have to add it as an argument everywhere.
    """

    # Drop all tables to ensure a clean state
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield # The tests run here