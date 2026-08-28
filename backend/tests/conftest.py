"""Shared pytest fixtures for CogniFlow tests."""

from __future__ import annotations

import os
from collections.abc import Callable, Generator

# ------------------------------------------------------------------
# IMPORTANT:
# Set the test database BEFORE importing app.database/models.
# This prevents the test suite from depending on the real PostgreSQL
# database.
# ------------------------------------------------------------------

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DEBUG"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.core.database import Base
from app.main import app
from app.models.developer import Developer
from app.models.event import Event
from app.seed.seed_developers import seed_developers
from app.seed.seed_tasks import seed_tasks
from app.seed.seed_teams import seed_teams


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Create an isolated SQLite database for one test."""

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    # Create all tables on the same connection that the tests will use.
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


@pytest.fixture
def client(
    db_session: Session,
) -> Generator[TestClient, None, None]:
    """Create a FastAPI test client using the isolated test DB."""

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def event_factory(
    db_session: Session,
) -> Callable[..., Event]:
    """
    Create and persist a realistic Event for analytics tests.

    The factory uses the first seeded developer and its team unless
    another developer is explicitly supplied.
    """

    developer = (
        db_session.query(Developer)
        .order_by(Developer.id)
        .first()
    )

    if developer is None:
        raise RuntimeError("Test developer was not seeded.")

    def create_event(
        *,
        timestamp,
        source: str,
        event_type: str,
        context: str,
        title: str | None = None,
        description: str | None = None,
        developer_id: int | None = None,
        team_id: int | None = None,
        task_id: int | None = None,
        related_developer_id: int | None = None,
        event_metadata: dict | None = None,
    ) -> Event:
        event = Event(
            developer_id=(
                developer_id
                if developer_id is not None
                else developer.id
            ),
            team_id=(
                team_id
                if team_id is not None
                else developer.team_id
            ),
            task_id=task_id,
            timestamp=timestamp,
            source=source,
            event_type=event_type,
            context=context,
            title=title or f"{source} activity",
            description=description,
            related_developer_id=related_developer_id,
            event_metadata=event_metadata,
        )

        db_session.add(event)
        db_session.flush()

        return event

    return create_event