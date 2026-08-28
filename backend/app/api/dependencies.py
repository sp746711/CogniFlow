"""
FastAPI dependencies for CogniFlow.

This module provides shared dependencies used by the API layer.

The database session itself is created by the database infrastructure
module so that every API route uses the same SQLAlchemy session
configuration.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import get_db as database_get_db


def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session to FastAPI endpoints.

    The actual session lifecycle is managed by
    app.core.database.get_db().

    This wrapper keeps the API dependency interface simple and
    preserves the existing imports used by CogniFlow API routes.
    """

    yield from database_get_db()