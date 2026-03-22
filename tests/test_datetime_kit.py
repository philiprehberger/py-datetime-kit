from datetime import date, datetime, timezone

from philiprehberger_datetime_kit import (
    business_days,
    date_range,
    end_of,
    relative,
    start_of,
)

UTC = timezone.utc


def test_business_days_basic():
    # Mon 2026-03-16 to Fri 2026-03-20 = 4 business days
    assert business_days("2026-03-16", "2026-03-20") == 4


def test_business_days_with_weekend():
    # Mon 2026-03-16 to Mon 2026-03-23 = 5 business days (skips Sat/Sun)
    assert business_days("2026-03-16", "2026-03-23") == 5


def test_business_days_with_holidays():
    # Mon-Fri but Wednesday is a holiday
    count = business_days(
        "2026-03-16",
        "2026-03-20",
        holidays=["2026-03-18"],
    )
    assert count == 3


def test_date_range():
    dates = list(date_range("2026-03-01", "2026-03-05"))
    assert dates == [
        date(2026, 3, 1),
        date(2026, 3, 2),
        date(2026, 3, 3),
        date(2026, 3, 4),
        date(2026, 3, 5),
    ]


def test_date_range_with_step():
    dates = list(date_range("2026-03-01", "2026-03-10", step=3))
    assert dates == [
        date(2026, 3, 1),
        date(2026, 3, 4),
        date(2026, 3, 7),
        date(2026, 3, 10),
    ]


def test_relative():
    result = relative(days=1)
    now = datetime.now(UTC)
    diff = result - now
    assert 0.9 < diff.total_seconds() / 86400 < 1.1


def test_start_of_day():
    dt = datetime(2026, 3, 21, 14, 30, 45, tzinfo=UTC)
    result = start_of("day", dt)
    assert result == datetime(2026, 3, 21, 0, 0, 0, tzinfo=UTC)


def test_start_of_month():
    dt = datetime(2026, 3, 21, 14, 30, 45, tzinfo=UTC)
    result = start_of("month", dt)
    assert result == datetime(2026, 3, 1, 0, 0, 0, tzinfo=UTC)


def test_end_of_day():
    dt = datetime(2026, 3, 21, 14, 30, 45, tzinfo=UTC)
    result = end_of("day", dt)
    assert result == datetime(2026, 3, 21, 23, 59, 59, 999999, tzinfo=UTC)


def test_end_of_month():
    dt = datetime(2026, 3, 21, 14, 30, 45, tzinfo=UTC)
    result = end_of("month", dt)
    assert result == datetime(2026, 3, 31, 23, 59, 59, 999999, tzinfo=UTC)
