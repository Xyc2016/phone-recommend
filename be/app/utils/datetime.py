"""Datetime helpers."""

from datetime import datetime, timedelta, timezone

BJ = timezone(timedelta(hours=8))


def now() -> datetime:
    return datetime.now(tz=BJ)