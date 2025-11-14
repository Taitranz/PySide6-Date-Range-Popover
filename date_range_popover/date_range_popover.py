from __future__ import annotations

from typing import Optional

from PyQt6.QtWidgets import QWidget

from .api.config import DatePickerConfig
from .api.picker import DateRangePicker


class DateRangePopover(DateRangePicker):
    """
    Turn-key widget that wraps :class:`DateRangePicker` for embedding.

    Importing :class:`DateRangePopover` keeps application code terse: it exposes
    the same public API as :class:`DateRangePicker` but ships with a default
    configuration, making it ideal for quick experiments and demos. Host
    applications are encouraged to pass a pre-sanitised :class:`DatePickerConfig`
    so constraints (min/max dates, layout bounds, themes) are explicit at
    construction time.
    """

    def __init__(
        self,
        config: Optional[DatePickerConfig] = None,
        parent: QWidget | None = None,
    ) -> None:
        """
        Build the popover using the provided configuration and optional parent.

        :param config: Optional :class:`DatePickerConfig`. Falls back to defaults.
        :param parent: Parent widget responsible for lifetime management.
        """
        super().__init__(config=config, parent=parent)


__all__ = ["DateRangePopover"]

