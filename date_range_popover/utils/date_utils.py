"""Date helper utilities used across the picker."""

from __future__ import annotations

from collections.abc import Iterator

from PySide6.QtCore import QDate

from ..exceptions import InvalidDateError


def copy_qdate(date: QDate) -> QDate:
    """Return a defensive copy of ``date``."""
    if not date.isValid():
        raise InvalidDateError(f"Cannot copy invalid QDate: {date}")
    return QDate(date)


def first_of_month(date: QDate) -> QDate:
    """Return the first day of the month for ``date``."""
    if not date.isValid():
        raise InvalidDateError(f"Cannot compute first of month for invalid QDate: {date}")
    return QDate(date.year(), date.month(), 1)


def qdate_to_ordinal(date: QDate) -> int:
    """Return a monotonically increasing integer representing ``date``."""
    if not date.isValid():
        raise InvalidDateError(f"Cannot convert invalid QDate to ordinal: {date}")
    return date.toJulianDay()


def qdate_is_before(left: QDate, right: QDate) -> bool:
    """Return ``True`` when ``left`` occurs before ``right``."""
    return qdate_to_ordinal(left) < qdate_to_ordinal(right)


def qdate_is_after(left: QDate, right: QDate) -> bool:
    """Return ``True`` when ``left`` occurs after ``right``."""
    return qdate_to_ordinal(left) > qdate_to_ordinal(right)


def normalize_range(start: QDate, end: QDate) -> tuple[QDate, QDate]:
    """Return an ordered tuple where ``start`` <= ``end``."""
    if not start.isValid() or not end.isValid():
        raise InvalidDateError("Both start and end dates must be valid QDate instances")
    if qdate_is_after(start, end):
        start, end = end, start
    return QDate(start), QDate(end)


def iter_month_days(month: QDate) -> Iterator[QDate]:
    """Yield ``QDate`` instances for each day in the visible month grid."""
    first = first_of_month(month)
    start_offset = (first.dayOfWeek() - 1) % 7
    start_date = first.addDays(-start_offset)
    for index in range(6 * 7):
        yield start_date.addDays(index)


__all__ = [
    "copy_qdate",
    "first_of_month",
    "normalize_range",
    "iter_month_days",
    "qdate_is_before",
    "qdate_is_after",
    "qdate_to_ordinal",
]
