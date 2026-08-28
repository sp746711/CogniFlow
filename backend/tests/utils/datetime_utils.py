"""Date and time utilities for CogniFlow."""

from __future__ import annotations

from datetime import datetime, time, timedelta


WORKDAY_START = time(hour=10, minute=0)
WORKDAY_END = time(hour=18, minute=0)


def combine_date_and_time(
    date_value: datetime,
    time_value: time,
) -> datetime:
    """Combine a date from a datetime with a specific time."""

    return datetime.combine(
        date_value.date(),
        time_value,
        tzinfo=date_value.tzinfo,
    )


def workday_start(work_date: datetime) -> datetime:
    """Return the simulated workday start at 10:00 AM."""

    return combine_date_and_time(
        work_date,
        WORKDAY_START,
    )


def workday_end(work_date: datetime) -> datetime:
    """Return the simulated workday end at 6:00 PM."""

    return combine_date_and_time(
        work_date,
        WORKDAY_END,
    )


def is_within_workday(timestamp: datetime) -> bool:
    """Return True when a timestamp falls inside 10 AM–6 PM."""

    current_time = timestamp.time()

    return WORKDAY_START <= current_time <= WORKDAY_END


def minutes_between(
    start: datetime,
    end: datetime,
) -> float:
    """Return elapsed time between two timestamps in minutes."""

    if end < start:
        raise ValueError(
            "End timestamp cannot be earlier than start timestamp."
        )

    return (end - start).total_seconds() / 60.0


def seconds_between(
    start: datetime,
    end: datetime,
) -> float:
    """Return elapsed time between two timestamps in seconds."""

    if end < start:
        raise ValueError(
            "End timestamp cannot be earlier than start timestamp."
        )

    return (end - start).total_seconds()


def add_minutes(
    timestamp: datetime,
    minutes: float,
) -> datetime:
    """Add a number of minutes to a timestamp."""

    return timestamp + timedelta(minutes=minutes)


def clamp_to_workday(
    timestamp: datetime,
    work_date: datetime,
) -> datetime:
    """Keep a timestamp inside the simulated 10 AM–6 PM workday."""

    start = workday_start(work_date)
    end = workday_end(work_date)

    if timestamp < start:
        return start

    if timestamp > end:
        return end

    return timestamp