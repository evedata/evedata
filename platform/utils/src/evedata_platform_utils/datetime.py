"""Datetime utility functions."""

from datetime import UTC, date, datetime
from email.utils import parsedate_to_datetime


def http_date_to_date(date_str: str | None) -> date | None:
    """Convert HTTP date header to date object in UTC.

    Args:
        date_str: HTTP date string (e.g., "Mon, 23 Jun 2025 12:34:56 GMT")

    Returns:
        date object in UTC or None if date_str is None or invalid
    """
    dt = http_date_to_datetime(date_str)
    if dt:
        return dt.date()
    return None


def http_date_to_datetime(date_str: str | None) -> datetime | None:
    """Convert HTTP date header to datetime object in UTC.

    Args:
        date_str: HTTP date string (e.g., "Mon, 23 Jun 2025 12:34:56 GMT")

    Returns:
        datetime object in UTC or None if date_str is None or invalid
    """
    if not date_str:
        return None

    try:
        # parsedate_to_datetime handles various HTTP date formats
        dt = parsedate_to_datetime(date_str)
    except (ValueError, TypeError):
        return None
    else:
        # Ensure UTC timezone
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        elif dt.tzinfo != UTC:
            dt = dt.astimezone(UTC)
        return dt


def http_date_to_iso8601(date_str: str | None) -> str | None:
    """Convert HTTP date header to ISO 8601 / RFC3339 format string in UTC.

    Args:
        date_str: HTTP date string (e.g., "Mon, 23 Jun 2025 12:34:56 GMT")

    Returns:
        ISO 8601 formatted string (e.g., "2025-06-23T12:34:56Z") or None
    """
    dt = http_date_to_datetime(date_str)
    if dt:
        # Use 'Z' suffix for UTC instead of '+00:00'
        return dt.isoformat().replace("+00:00", "Z")
    return None
