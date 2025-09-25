"""
Central configuration and fixtures for the pytest test suite.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from daily_briefing.database import Base, DATABASE_URL

# This engine is created using the DATABASE_URL from the main application code.
# The URL is built from environment variables, which allows the CI pipeline
# to point this to a test-specific database.
engine = create_engine(DATABASE_URL)

# This sessionmaker is configured once and imported by tests that need to
# interact with the database directly.
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_session_setup():
    """
    A session-scoped, auto-used fixture to manage the test database schema.

    This fixture will run only once per test session for tests that request it.
    It ensures the database is in a clean state by dropping all existing tables
    and then recreating them based on the current models. This guarantees
    that tests run against a predictable and consistent database schema.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield