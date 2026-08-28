"""Analytics metric model for CogniFlow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.developer import Developer


class Metric(Base):
    """
    Stores a calculated CogniFlow analytics metric.

    Metrics can represent developer-level or broader dashboard
    measurements. The actual formulas are calculated later by the
    analytics services.
    """

    __tablename__ = "metrics"

    # ==============================================================
    # PRIMARY KEY
    # ==============================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    # ==============================================================
    # OPTIONAL DEVELOPER
    # ==============================================================

    developer_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "developers.id",
            ondelete="CASCADE",
        ),
        nullable=True,
        index=True,
    )

    # ==============================================================
    # METRIC INFORMATION
    # ==============================================================

    metric_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )

    scope: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # ==============================================================
    # CALCULATION TIME
    # ==============================================================

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==============================================================
    # OPTIONAL ANALYSIS PERIOD
    # ==============================================================

    period_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    period_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ==============================================================
    # DESCRIPTION
    # ==============================================================

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==============================================================
    # RELATIONSHIP
    # ==============================================================

    developer: Mapped["Developer | None"] = relationship(
        "Developer",
        back_populates="metrics",
    )