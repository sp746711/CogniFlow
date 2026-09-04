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

# Active dialect tracking ('postgresql' or 'sqlite')
CURRENT_DB_DIALECT = "postgresql"


def _create_db_engine(url: str) -> Engine:
    """
    Helper to create engine with appropriate kwargs depending on dialect.
    """
    if url.startswith("sqlite"):
        return create_engine(
            url,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False},
        )
    return create_engine(
        url,
        echo=settings.DEBUG,
        pool_pre_ping=True,
    )


# Primary engine creation
try:
    engine: Engine = _create_db_engine(DATABASE_URL)
    # Test primary engine connection
    with engine.connect() as _conn:
        _conn.execute(text("SELECT 1"))
except Exception as psql_err:
    # If in development or postgresql unreachable, fallback to SQLite
    sqlite_url = "sqlite:///./cogniflow_dev.db"
    print(f"[CogniFlow DB Warning] Could not connect to PostgreSQL ({psql_err}).")
    print(f"[CogniFlow DB Info] Falling back to SQLite database at {sqlite_url}")
    DATABASE_URL = sqlite_url
    CURRENT_DB_DIALECT = "sqlite"
    engine = _create_db_engine(DATABASE_URL)


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


def get_db_dialect() -> str:
    """Return the active database dialect name ('postgresql' or 'sqlite')."""
    return CURRENT_DB_DIALECT


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
    Check whether the active database is reachable.

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
# AUTOMATIC SCHEMA & SEED HELPER (FOR DEV/FALLBACK)
# ==============================================================


def ensure_database_ready() -> None:
    """
    Ensure database tables exist and seed initial demo data if empty.
    """
    create_database_tables()

    # Check if teams table has data
    db = SessionLocal()
    try:
        from app.models.team import Team
        team_count = db.query(Team).count()
        if team_count == 0:
            print("[CogniFlow DB Info] Database is empty. Seeding initial demo data...")
            from app.seed.seed_teams import seed_teams
            from app.seed.seed_developers import seed_developers
            from app.seed.seed_tasks import seed_tasks

            seed_teams(db)
            seed_developers(db)
            seed_tasks(db)
            print("[CogniFlow DB Info] Database seeding completed successfully.")
    except Exception as err:
        print(f"[CogniFlow DB Warning] Database readiness check note: {err}")
    finally:
        db.close()


# ==============================================================
# DATABASE SESSION HEALTH CHECK
# ==============================================================


def verify_database() -> None:
    """
    Verify the database connection.

    Raises:
        RuntimeError: when database cannot be reached.
    """

    if not check_database_connection():
        raise RuntimeError(
            "CogniFlow could not connect to the database."
        )