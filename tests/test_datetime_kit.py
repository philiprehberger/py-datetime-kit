from datetime import date, datetime, timedelta, timezone

from philiprehberger_datetime_kit import (
    add_business_days,
    business_days,
    date_range,
    end_of,
    format_duration,
    is_weekend,
    next_business_day,
    relative,
    start_of,
    time_ago,
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


def test_add_business_days_forward():
    result = add_business_days("2026-04-06", 3)  # Monday
    assert result == date(2026, 4, 9)  # Thursday


def test_add_business_days_over_weekend():
    result = add_business_days("2026-04-09", 2)  # Thursday
    assert result == date(2026, 4, 13)  # Monday


def test_add_business_days_with_holidays():
    result = add_business_days("2026-04-06", 3, holidays=["2026-04-07"])
    assert result == date(2026, 4, 10)  # skips Tuesday holiday


def test_add_business_days_negative():
    result = add_business_days("2026-04-09", -2)  # Thursday
    assert result == date(2026, 4, 7)  # Tuesday


def test_time_ago_just_now():
    now = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)
    assert time_ago(now, now=now) == "just now"


def test_time_ago_minutes():
    now = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)
    dt = now - timedelta(minutes=5)
    assert time_ago(dt, now=now) == "5 minutes ago"


def test_time_ago_hours():
    now = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)
    dt = now - timedelta(hours=3)
    assert time_ago(dt, now=now) == "3 hours ago"


def test_time_ago_days():
    now = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)
    dt = now - timedelta(days=7)
    assert time_ago(dt, now=now) == "7 days ago"


def test_time_ago_singular():
    now = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc)
    dt = now - timedelta(hours=1)
    assert time_ago(dt, now=now) == "1 hour ago"


def test_format_duration_seconds():
    assert format_duration(45) == "45s"


def test_format_duration_minutes_seconds():
    assert format_duration(150) == "2m 30s"


def test_format_duration_hours():
    assert format_duration(3661) == "1h 1m 1s"


def test_format_duration_days():
    assert format_duration(90061) == "1d 1h 1m 1s"


def test_format_duration_milliseconds():
    assert format_duration(0.5) == "500ms"


def test_format_duration_zero():
    assert format_duration(0) == "0ms"
