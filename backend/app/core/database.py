"""
CogniFlow database configuration.

This module provides:

- SQLAlchemy declarative Base
- PostgreSQL engine
- Synchronous session factory
- FastAPI database dependency
- Database connection helper
- Database shutdown helper

CogniFlow uses PostgreSQL for persistent application data.

The application uses simulated/demo activity only. No real
Slack, Jira, GitHub, or IDE credentials are required.

Database schema creation and migrations are handled separately
through Alembic.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings


# ==============================================================
# SQLALCHEMY BASE
# ==============================================================


class Base(DeclarativeBase):
    """
    Base class for all CogniFlow SQLAlchemy models.

    All database models inherit from this class.

    Current models include:

    - Team
    - Developer
    - Task
    - Event
    - FlowSession
    - Interruption
    - ContextSwitch
    - Metric
    """

    pass


# ==============================================================
# DATABASE URL
# ==============================================================


def _get_sync_database_url(database_url: str) -> str:
    """
    Convert supported PostgreSQL URLs into a synchronous
    SQLAlchemy PostgreSQL URL.

    CogniFlow's original configuration may contain:

        postgresql+asyncpg://

    because the initial database implementation used AsyncSQLAlchemy.

    The current CogniFlow service/API architecture uses synchronous
    SQLAlchemy sessions, so the URL is converted to:

        postgresql+psycopg://

    Plain PostgreSQL URLs are also normalized.
    """

    url = database_url.strip()

    if not url:
        raise ValueError(
            "DATABASE_URL cannot be empty."
        )

    if url.startswith(
        "postgresql+asyncpg://"
    ):
        return url.replace(
            "postgresql+asyncpg://",
            "postgresql+psycopg://",
            1,
        )

    if url.startswith(
        "postgresql://"
    ):
        return url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    if url.startswith(
        "postgres://"
    ):
        return url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    return url


DATABASE_URL = _get_sync_database_url(
    settings.DATABASE_URL
)


# ==============================================================
# DATABASE ENGINE
# ==============================================================


engine: Engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


# ==============================================================
# SESSION FACTORY
# ==============================================================


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# ==============================================================
# FASTAPI DATABASE DEPENDENCY
# ==============================================================


def get_db() -> Generator[Session, None, None]:
    """
    Provide one database session for a FastAPI request.

    The session is automatically closed after the request.

    If an exception occurs while processing the request, the
    current transaction is rolled back before the exception
    is re-raised.
    """

    db = SessionLocal()

    try:
        yield db

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# ==============================================================
# DATABASE CONNECTION CHECK
# ==============================================================


def check_database_connection() -> bool:
    """
    Check whether PostgreSQL is reachable.

    Returns:
        True when the database responds successfully.
        False when the connection/check fails.
    """

    try:
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

        return True

    except Exception:
        return False


# ==============================================================
# DATABASE SHUTDOWN
# ==============================================================


def close_database() -> None:
    """
    Dispose the SQLAlchemy engine.

    This should be called when the FastAPI application
    shuts down.
    """

    engine.dispose()


# ==============================================================
# OPTIONAL DATABASE INITIALIZATION HELPER
# ==============================================================


def create_database_tables() -> None:
    """
    Create all registered SQLAlchemy tables.

    This helper is intentionally separate from application startup.

    CogniFlow's normal production/development schema management
    should use Alembic migrations.

    This function is useful for local testing when a developer
    explicitly wants SQLAlchemy to create the schema.
    """

    # Import models so that all model classes are registered
    # with Base.metadata before create_all() is called.
    import app.models  # noqa: F401

    Base.metadata.create_all(
        bind=engine
    )


# ==============================================================
# DATABASE SESSION HEALTH CHECK
# ==============================================================


def verify_database() -> None:
    """
    Verify the database connection.

    Raises:
        RuntimeError: when PostgreSQL cannot be reached.
    """

    if not check_database_connection():
        raise RuntimeError(
            "CogniFlow could not connect to the PostgreSQL database."
        )