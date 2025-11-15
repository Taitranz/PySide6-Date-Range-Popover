"""Unit tests for helpers in date_range_popover.core.state_logic."""

from __future__ import annotations

from date_range_popover.core.state_logic import clamp_visible_month
from PySide6.QtCore import QDate


def _first_day(date: QDate) -> QDate:
    return QDate(date.year(), date.month(), 1)


def test_clamp_visible_month_respects_min_bound() -> None:
    """Months before the allowed window should clamp to min_date."""
    min_date = QDate(2024, 6, 15)
    requested_month = QDate(2024, 1, 5)

    result = clamp_visible_month(requested_month, min_date, None)

    assert result == _first_day(min_date)


def test_clamp_visible_month_respects_max_bound() -> None:
    """Months after the allowed window should clamp to max_date."""
    max_date = QDate(2024, 3, 20)
    requested_month = QDate(2024, 10, 1)

    result = clamp_visible_month(requested_month, None, max_date)

    assert result == _first_day(max_date)
