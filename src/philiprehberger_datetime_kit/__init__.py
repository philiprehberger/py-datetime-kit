"""Common datetime operations missing from the standard library."""

from __future__ import annotations

import calendar
from collections.abc import Generator
from datetime import date, datetime, timedelta, timezone

__all__ = [
    "business_days",
    "date_range",
    "end_of",
    "is_weekend",
    "next_business_day",
    "relative",
    "start_of",
]

_UTC = timezone.utc


def _to_date(value: str | date) -> date:
    """Convert a string or date to a date object."""
    if isinstance(value, str):
        return date.fromisoformat(value)
    if isinstance(value, datetime):
        return value.date()
    return value


def business_days(
    start: str | date,
    end: str | date,
    holidays: list[str | date] | None = None,
) -> int:
    """Count business days (Mon-Fri) between two dates, exclusive of end.

    Args:
        start: Start date as ISO string or date object.
        end: End date as ISO string or date object.
        holidays: Optional list of dates to exclude from the count.

    Returns:
        Number of business days between start and end.
    """
    start_d = _to_date(start)
    end_d = _to_date(end)

    holiday_set: set[date] = set()
    if holidays:
        holiday_set = {_to_date(h) for h in holidays}

    if start_d > end_d:
        start_d, end_d = end_d, start_d

    count = 0
    current = start_d
    while current < end_d:
        if current.weekday() < 5 and current not in holiday_set:
            count += 1
        current += timedelta(days=1)

    return count


def date_range(
    start: str | date,
    end: str | date,
    step: int = 1,
) -> Generator[date]:
    """Yield dates from start to end inclusive.

    Args:
        start: Start date as ISO string or date object.
        end: End date as ISO string or date object.
        step: Number of days between each yielded date.

    Yields:
        Date objects from start through end.
    """
    current = _to_date(start)
    end_d = _to_date(end)
    delta = timedelta(days=step)

    while current <= end_d:
        yield current
        current += delta


def relative(
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> datetime:
    """Return the current UTC time offset by the given delta.

    Args:
        days: Number of days to offset.
        hours: Number of hours to offset.
        minutes: Number of minutes to offset.
        seconds: Number of seconds to offset.

    Returns:
        A timezone-aware UTC datetime.
    """
    return datetime.now(_UTC) + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )


def start_of(unit: str, dt: datetime | None = None) -> datetime:
    """Return the start of the given time unit.

    Supported units: ``"day"``, ``"week"``, ``"month"``, ``"year"``.

    Args:
        unit: The time unit to truncate to.
        dt: The reference datetime. Defaults to now (UTC).

    Returns:
        A timezone-aware UTC datetime at the start of the unit.
    """
    if dt is None:
        dt = datetime.now(_UTC)

    match unit:
        case "day":
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        case "week":
            monday = dt - timedelta(days=dt.weekday())
            return monday.replace(hour=0, minute=0, second=0, microsecond=0)
        case "month":
            return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        case "year":
            return dt.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0,
            )
        case _:
            msg = f"Unsupported unit: {unit!r}. Use 'day', 'week', 'month', or 'year'."
            raise ValueError(msg)


def is_weekend(dt: date | datetime | None = None) -> bool:
    """Check if a date falls on a weekend (Saturday or Sunday).

    Args:
        dt: The date to check. Defaults to today.

    Returns:
        True if the date is a Saturday or Sunday.
    """
    d = dt or date.today()
    if isinstance(d, datetime):
        d = d.date()
    return d.weekday() >= 5


def next_business_day(
    dt: date | datetime | None = None,
    holidays: list[date] | None = None,
) -> date:
    """Return the next business day (Mon-Fri, excluding holidays).

    Args:
        dt: The reference date. Defaults to today.
        holidays: Optional list of dates to skip.

    Returns:
        The next date that is a weekday and not in the holiday list.
    """
    d = dt or date.today()
    if isinstance(d, datetime):
        d = d.date()
    holiday_set = set(holidays) if holidays else set()
    candidate = d + timedelta(days=1)
    while candidate.weekday() >= 5 or candidate in holiday_set:
        candidate += timedelta(days=1)
    return candidate


def end_of(unit: str, dt: datetime | None = None) -> datetime:
    """Return the end of the given time unit.

    Supported units: ``"day"``, ``"week"``, ``"month"``, ``"year"``.

    Args:
        unit: The time unit.
        dt: The reference datetime. Defaults to now (UTC).

    Returns:
        A timezone-aware UTC datetime at the end of the unit
        (23:59:59.999999).
    """
    if dt is None:
        dt = datetime.now(_UTC)

    match unit:
        case "day":
            return dt.replace(
                hour=23, minute=59, second=59, microsecond=999999,
            )
        case "week":
            sunday = dt + timedelta(days=6 - dt.weekday())
            return sunday.replace(
                hour=23, minute=59, second=59, microsecond=999999,
            )
        case "month":
            last_day = calendar.monthrange(dt.year, dt.month)[1]
            return dt.replace(
                day=last_day, hour=23, minute=59, second=59, microsecond=999999,
            )
        case "year":
            return dt.replace(
                month=12, day=31, hour=23, minute=59, second=59,
                microsecond=999999,
            )
        case _:
            msg = f"Unsupported unit: {unit!r}. Use 'day', 'week', 'month', or 'year'."
            raise ValueError(msg)
