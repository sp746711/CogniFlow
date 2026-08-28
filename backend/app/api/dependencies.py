"""FastAPI dependencies for CogniFlow."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide a database session to FastAPI endpoints.

    The session is created for the request and always closed afterward.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()