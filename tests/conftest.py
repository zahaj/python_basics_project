import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from daily_briefing.database import Base, DATABASE_URL

# For tests, we'll connect to a separate test database
# The environment variables will be set by the CI runner
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def db_session_setup():
    """
    A session-scoped fixture to set up the database once for all tests
    that need it.git
    """

    # Drop all tables to ensure a clean state
    Base.metadata.drop_all(bind=engine)
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield # The tests run here