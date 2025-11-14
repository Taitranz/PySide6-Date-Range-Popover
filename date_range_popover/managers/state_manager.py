from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, auto
from typing import Tuple, cast

from PyQt6.QtCore import QDate, QObject, pyqtSignal

from ..exceptions import InvalidDateError
from ..validation import validate_date_range, validate_qdate
from ..utils import first_of_month, get_logger

LOGGER = get_logger(__name__)


class PickerMode(Enum):
    """Supported picker modes exposed via the public API."""

    DATE = auto()
    CUSTOM_RANGE = auto()


@dataclass(frozen=True, slots=True)
class DatePickerState:
    """
    Immutable snapshot of the picker state.

    Instances are emitted via the ``state_changed`` signal so observers can
    derive view models without mutating internal structures. All ``QDate``
    objects are defensive copies to avoid lifetime issues.
    """

    mode: PickerMode
    selected_dates: Tuple[QDate | None, QDate | None]
    visible_month: QDate


class DatePickerStateManager(QObject):
    """
    Centralized store for picker state.

    The manager owns the authoritative selection, mode, and visible month. It
    enforces ``min_date``/``max_date`` bounds, emits granular signals for UI
    components, and exposes a small mutator surface (`select_date`,
    `select_range`, `set_mode`, `set_visible_month`, `reset`). This class is an
    internal detail—public consumers interact with :class:`DateRangePicker`
    instead—but documenting it clarifies extension points for advanced users.
    """

    mode_changed = pyqtSignal(PickerMode)
    selected_date_changed = pyqtSignal(QDate)
    selected_range_changed = pyqtSignal(QDate, QDate)
    visible_month_changed = pyqtSignal(QDate)
    state_changed = pyqtSignal(DatePickerState)

    def __init__(self, *, min_date: QDate | None = None, max_date: QDate | None = None) -> None:
        """
        Build a new state manager with optional selection bounds.

        :param min_date: Lower bound; ``None`` means unbounded.
        :param max_date: Upper bound; ``None`` means unbounded.
        :raises InvalidDateError: If ``min_date`` is after ``max_date``.
        """
        super().__init__()
        self._min_date = QDate(min_date) if isinstance(min_date, QDate) else None
        self._max_date = QDate(max_date) if isinstance(max_date, QDate) else None
        if self._min_date is not None and self._max_date is not None and self._min_date > self._max_date:
            raise InvalidDateError("min_date must be on or before max_date")
        initial_date = self._default_selection_date()
        self._state = DatePickerState(
            mode=PickerMode.DATE,
            selected_dates=(initial_date, None),
            visible_month=first_of_month(initial_date),
        )

    @property
    def state(self) -> DatePickerState:
        """Latest immutable snapshot used by coordinators and widgets."""
        return self._state

    @property
    def min_date(self) -> QDate | None:
        """Configured lower bound for selection/navigation (defensive copy)."""
        return self._min_date

    @property
    def max_date(self) -> QDate | None:
        """Configured upper bound for selection/navigation (defensive copy)."""
        return self._max_date

    def set_mode(self, mode: PickerMode) -> None:
        """
        Update the active picker mode and notify listeners.

        :param mode: Desired :class:`PickerMode`.
        """
        if mode is self._state.mode:
            return
        LOGGER.debug("Picker mode change: %s -> %s", self._state.mode.name, mode.name)
        self._update_state(mode=mode)
        self.mode_changed.emit(mode)
        self.state_changed.emit(self._state)

    def select_date(self, date: QDate) -> None:
        """
        Select a single date and clear any existing range selection.

        :param date: Candidate ``QDate`` (must be valid and within bounds).
        """
        validated = cast(QDate, validate_qdate(date, field_name="selected_date"))
        validated = self._ensure_within_bounds(validated, "selected_date")
        LOGGER.debug("Selecting date: %s", validated.toString("yyyy-MM-dd"))
        current_start, current_end = self._state.selected_dates
        if current_start == validated and current_end is None:
            return
        self._update_state(
            selected_dates=(validated, None),
            visible_month=first_of_month(validated),
        )
        self.selected_date_changed.emit(validated)
        self.visible_month_changed.emit(self._state.visible_month)
        self.state_changed.emit(self._state)

    def select_range(self, start: QDate, end: QDate) -> None:
        """
        Select a date range (inclusive) and emit corresponding signals.

        :param start: Range start (inclusive).
        :param end: Range end (inclusive).
        """
        start_candidate, end_candidate = validate_date_range(
            start,
            end,
            field_name="selected_range",
            allow_partial=False,
        )
        validated_start = cast(QDate, start_candidate)
        validated_end = cast(QDate, end_candidate)
        validated_start = self._ensure_within_bounds(validated_start, "selected_range.start")
        validated_end = self._ensure_within_bounds(validated_end, "selected_range.end")
        LOGGER.debug(
            "Selecting range: %s -> %s",
            validated_start.toString("yyyy-MM-dd"),
            validated_end.toString("yyyy-MM-dd"),
        )
        self._update_state(
            selected_dates=(validated_start, validated_end),
            visible_month=first_of_month(validated_start),
        )
        self.selected_range_changed.emit(validated_start, validated_end)
        self.visible_month_changed.emit(self._state.visible_month)
        self.state_changed.emit(self._state)

    def set_visible_month(self, month: QDate) -> None:
        """
        Change the month displayed in the calendar UI.

        :param month: Any ``QDate`` within the desired month/year.
        """
        validated_month = cast(QDate, validate_qdate(month, field_name="visible_month"))
        target = self._clamp_visible_month(validated_month)
        LOGGER.debug("Updating visible month to %s", target.toString("yyyy-MM"))
        if target == self._state.visible_month:
            return
        self._update_state(visible_month=target)
        self.visible_month_changed.emit(target)
        self.state_changed.emit(self._state)

    def reset(self) -> None:
        """Reset the internal state to today's date in ``DATE`` mode."""
        default_date = self._default_selection_date()
        LOGGER.debug("Resetting picker state to %s", default_date.toString("yyyy-MM-dd"))
        self._update_state(
            mode=PickerMode.DATE,
            selected_dates=(default_date, None),
            visible_month=first_of_month(default_date),
        )
        self.mode_changed.emit(self._state.mode)
        self.selected_date_changed.emit(default_date)
        self.visible_month_changed.emit(self._state.visible_month)
        self.state_changed.emit(self._state)

    def _update_state(
        self,
        *,
        mode: PickerMode | None = None,
        selected_dates: Tuple[QDate | None, QDate | None] | None = None,
        visible_month: QDate | None = None,
    ) -> None:
        """Replace the immutable state with a new instance."""
        new_state = replace(
            self._state,
            mode=mode if mode is not None else self._state.mode,
            selected_dates=selected_dates if selected_dates is not None else self._state.selected_dates,
            visible_month=visible_month if visible_month is not None else self._state.visible_month,
        )
        self._state = new_state

    def _default_selection_date(self) -> QDate:
        """Return today's date clamped to the configured bounds."""
        return self._clamp_to_bounds(QDate.currentDate())

    def _ensure_within_bounds(self, date: QDate, field_name: str) -> QDate:
        """Validate that ``date`` sits within the configured bounds."""
        if self._min_date is not None and date < self._min_date:
            raise InvalidDateError(f"{field_name} must be on or after the configured min_date")
        if self._max_date is not None and date > self._max_date:
            raise InvalidDateError(f"{field_name} must be on or before the configured max_date")
        return date

    def _clamp_to_bounds(self, date: QDate) -> QDate:
        """Clamp ``date`` to ``min_date``/``max_date`` without raising."""
        result = QDate(date)
        if self._min_date is not None and result < self._min_date:
            result = QDate(self._min_date)
        if self._max_date is not None and result > self._max_date:
            result = QDate(self._max_date)
        return result

    def _clamp_visible_month(self, month: QDate) -> QDate:
        """Clamp a month to the allowed range (first-of-month resolution)."""
        target = first_of_month(month)
        if self._min_date is not None:
            min_month = first_of_month(self._min_date)
            if target < min_month:
                return min_month
        if self._max_date is not None:
            max_month = first_of_month(self._max_date)
            if target > max_month:
                return max_month
        return target

__all__ = ["DatePickerStateManager", "DatePickerState", "PickerMode"]


