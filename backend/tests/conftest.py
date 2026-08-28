"""Shared pytest fixtures for CogniFlow tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base
from app.seed.seed_developers import seed_developers
from app.seed.seed_tasks import seed_tasks
from app.seed.seed_teams import seed_teams


# SQLite is used only for automated tests.
# The actual CogniFlow application uses PostgreSQL.
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session() -> Session:
    """Create an isolated database session for one test."""

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        seed_teams(db)
        seed_developers(db)
        seed_tasks(db)

        db.commit()

        yield db

    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()