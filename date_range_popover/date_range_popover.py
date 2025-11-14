from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QWidget

from .api.config import DatePickerConfig
from .api.picker import DateRangePicker


class DateRangePopover(DateRangePicker):
    """Primary popover widget that exposes the DateRangePicker facade."""

    def __init__(
        self,
        config: Optional[DatePickerConfig] = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(config=config, parent=parent)


__all__ = ["DateRangePopover"]

