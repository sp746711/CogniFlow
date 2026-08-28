"""
CogniFlow database configuration.

This module provides:

- SQLAlchemy declarative Base
- Async PostgreSQL engine
- Async session factory
- FastAPI database dependency
- Database connection helper

Database schema creation/migrations will be handled later through
the project's migration workflow. This file only provides the
database infrastructure.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# ==============================================================
# SQLALCHEMY BASE
# ==============================================================


class Base(DeclarativeBase):
    """
    Base class for all CogniFlow SQLAlchemy models.

    Future models such as Team, Developer, Event, Task,
    FlowSession, Interruption, ContextSwitch and Metric
    will inherit from this Base.
    """

    pass


# ==============================================================
# DATABASE ENGINE
# ==============================================================


engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


# ==============================================================
# SESSION FACTORY
# ==============================================================


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# ==============================================================
# FASTAPI DATABASE DEPENDENCY
# ==============================================================


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide one database session for a FastAPI request.

    The session is automatically closed when the request finishes.
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# ==============================================================
# DATABASE CONNECTION CHECK
# ==============================================================


async def check_database_connection() -> bool:
    """
    Check whether PostgreSQL is reachable.

    Returns:
        True when the database responds successfully.
        False when the connection/check fails.
    """

    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        return True

    except Exception:
        return False


# ==============================================================
# DATABASE SHUTDOWN
# ==============================================================


async def close_database() -> None:
    """
    Dispose the SQLAlchemy engine.

    This should be called when the FastAPI application shuts down.
    """

    await engine.dispose()