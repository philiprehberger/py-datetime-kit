from datetime import date, datetime, timezone

from philiprehberger_datetime_kit import (
    business_days,
    date_range,
    end_of,
    is_weekend,
    next_business_day,
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


def test_is_weekend_saturday():
    assert is_weekend(date(2026, 4, 4)) is True  # Saturday


def test_is_weekend_sunday():
    assert is_weekend(date(2026, 4, 5)) is True  # Sunday


def test_is_weekend_weekday():
    assert is_weekend(date(2026, 4, 6)) is False  # Monday


def test_is_weekend_with_datetime():
    dt = datetime(2026, 4, 4, 12, 0, 0, tzinfo=UTC)  # Saturday
    assert is_weekend(dt) is True


def test_next_business_day_from_weekday():
    # Wednesday -> Thursday
    result = next_business_day(date(2026, 4, 1))
    assert result == date(2026, 4, 2)


def test_next_business_day_from_friday():
    # Friday -> Monday
    result = next_business_day(date(2026, 4, 3))
    assert result == date(2026, 4, 6)


def test_next_business_day_from_saturday():
    # Saturday -> Monday
    result = next_business_day(date(2026, 4, 4))
    assert result == date(2026, 4, 6)


def test_next_business_day_with_holidays():
    # Friday -> skip Sat, Sun, skip Monday holiday -> Tuesday
    result = next_business_day(date(2026, 4, 3), holidays=[date(2026, 4, 6)])
    assert result == date(2026, 4, 7)


def test_next_business_day_with_datetime():
    dt = datetime(2026, 4, 3, 15, 30, 0, tzinfo=UTC)  # Friday
    result = next_business_day(dt)
    assert result == date(2026, 4, 6)
