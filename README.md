# philiprehberger-datetime-kit

[![Tests](https://github.com/philiprehberger/py-datetime-kit/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-datetime-kit/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-datetime-kit.svg)](https://pypi.org/project/philiprehberger-datetime-kit/)
[![License](https://img.shields.io/github/license/philiprehberger/py-datetime-kit)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Common datetime operations missing from the standard library.

## Installation

```bash
pip install philiprehberger-datetime-kit
```

## Usage

```python
from philiprehberger_datetime_kit import business_days, date_range, relative

# Count business days between two dates
count = business_days("2026-03-16", "2026-03-20")  # 4
```

### Business Days with Holidays

```python
from philiprehberger_datetime_kit import business_days

count = business_days("2026-03-16", "2026-03-20", holidays=["2026-03-18"])  # 3
```

### Date Range

```python
from philiprehberger_datetime_kit import date_range

for d in date_range("2026-03-01", "2026-03-05"):
    print(d)
```

### Relative Time

```python
from philiprehberger_datetime_kit import relative

tomorrow = relative(days=1)
one_hour_ago = relative(hours=-1)
```

### Start and End of Period

```python
from philiprehberger_datetime_kit import start_of, end_of

start = start_of("month")   # first moment of current month
end = end_of("day")         # last moment of today
```

## API

| Function | Description |
|----------|-------------|
| `business_days(start, end, holidays?)` | Count business days (Mon-Fri) between two dates |
| `date_range(start, end, step?)` | Yield dates from start to end inclusive |
| `relative(days?, hours?, minutes?, seconds?)` | Return UTC now offset by the given delta |
| `start_of(unit, dt?)` | Start of day/week/month/year |
| `end_of(unit, dt?)` | End of day/week/month/year |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
