"""Tests for datetime utility functions."""

from datetime import UTC, datetime

import pytest

from evedata_utils.datetime import (
    http_date_to_datetime,
    http_date_to_iso8601,
)


class TestHttpDateToDatetime:
    @pytest.mark.parametrize(
        ("date_str", "expected"),
        [
            # RFC 7231 format (standard HTTP date)
            (
                "Mon, 23 Jun 2025 12:34:56 GMT",
                datetime(2025, 6, 23, 12, 34, 56, tzinfo=UTC),
            ),
            # RFC 850 format (obsolete but still supported)
            (
                "Monday, 23-Jun-25 12:34:56 GMT",
                datetime(2025, 6, 23, 12, 34, 56, tzinfo=UTC),
            ),
            # ANSI C asctime() format
            (
                "Mon Jun 23 12:34:56 2025",
                datetime(2025, 6, 23, 12, 34, 56, tzinfo=UTC),
            ),
            # None input
            (None, None),
            # Empty string
            ("", None),
        ],
    )
    def test_valid_dates(self, date_str: str | None, expected: datetime | None) -> None:
        result = http_date_to_datetime(date_str)
        assert result == expected

    def test_invalid_date_format(self) -> None:
        result = http_date_to_datetime("not a valid date")
        assert result is None

    def test_timezone_conversion(self) -> None:
        # Test with different timezone offset
        date_str = "Mon, 23 Jun 2025 12:34:56 -0500"
        result = http_date_to_datetime(date_str)
        assert result is not None
        assert result.tzinfo == UTC
        # Should be converted to UTC (5 hours ahead)
        assert result == datetime(2025, 6, 23, 17, 34, 56, tzinfo=UTC)


class TestHttpDateToIso8601:
    @pytest.mark.parametrize(
        ("date_str", "expected"),
        [
            # RFC 7231 format
            (
                "Mon, 23 Jun 2025 12:34:56 GMT",
                "2025-06-23T12:34:56Z",
            ),
            # RFC 850 format
            (
                "Monday, 23-Jun-25 12:34:56 GMT",
                "2025-06-23T12:34:56Z",
            ),
            # ANSI C asctime() format
            (
                "Mon Jun 23 12:34:56 2025",
                "2025-06-23T12:34:56Z",
            ),
            # None input
            (None, None),
            # Empty string
            ("", None),
        ],
    )
    def test_valid_dates(self, date_str: str | None, expected: str | None) -> None:
        result = http_date_to_iso8601(date_str)
        assert result == expected

    def test_invalid_date_format(self) -> None:
        result = http_date_to_iso8601("not a valid date")
        assert result is None

    def test_timezone_conversion(self) -> None:
        # Test with different timezone offset
        date_str = "Mon, 23 Jun 2025 12:34:56 -0500"
        result = http_date_to_iso8601(date_str)
        # Should be converted to UTC (5 hours ahead)
        assert result == "2025-06-23T17:34:56Z"

    def test_output_format_is_rfc3339(self) -> None:
        date_str = "Mon, 23 Jun 2025 12:34:56 GMT"
        result = http_date_to_iso8601(date_str)
        assert result is not None
        # RFC3339 format should use 'Z' for UTC
        assert result.endswith("Z")
        # Verify the timestamp format (excluding the 'Z')
        assert result == "2025-06-23T12:34:56Z"
