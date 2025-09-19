"""
Central configuration and fixtures for the pytest test suite.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from daily_briefing.database import Base

# This URL points to the database for local integration testing. It matches
# the database name in docker-compose.yml. The CI pipeline will override
# the database name to 'briefing_db_test' for safety.
TEST_DATABASE_URL = "postgresql+psycopg2://briefing_user:a_secure_password@localhost:5432/briefing_db"

# This sessionmaker is configured once and imported by tests that need to
# interact with the database directly.
engine = create_engine(TEST_DATABASE_URL)
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