"""Sliding track widget that hosts the animated indicator."""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..styles.constants import (
    DEFAULT_TRACK_WIDTH,
    SLIDING_INDICATOR_HEIGHT,
    SLIDING_INDICATOR_RADIUS,
    TRACK_BACKGROUND,
    TRACK_INDICATOR_COLOR,
    WINDOW_BACKGROUND,
)


class SlidingTrackIndicator(QWidget):
    """Handles layout of the sliding indicator within its track."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {WINDOW_BACKGROUND};")

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        self._track_container = QWidget(self)
        self._track_container.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._track_container.setStyleSheet(
            f"background-color: {TRACK_BACKGROUND}; border-radius: {SLIDING_INDICATOR_RADIUS}px;"
        )
        self._track_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self._track_container.setFixedHeight(SLIDING_INDICATOR_HEIGHT)

        track_layout = QHBoxLayout(self._track_container)
        track_layout.setContentsMargins(0, 0, 0, 0)
        track_layout.setSpacing(0)

        self._left_spacer = QWidget(self._track_container)
        self._left_spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._left_spacer.setFixedWidth(0)

        self._indicator = QWidget(self._track_container)
        self._indicator.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._indicator.setStyleSheet(
            f"background-color: {TRACK_INDICATOR_COLOR}; border-radius: {SLIDING_INDICATOR_RADIUS}px;"
        )
        self._indicator.setFixedHeight(SLIDING_INDICATOR_HEIGHT)

        self._right_spacer = QWidget(self._track_container)
        self._right_spacer.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._right_spacer.setFixedWidth(0)

        track_layout.addWidget(self._left_spacer)
        track_layout.addWidget(self._indicator)
        track_layout.addWidget(self._right_spacer)

        wrapper_layout.addWidget(self._track_container)

        self._current_position = 0
        self._current_width = 0

    @property
    def current_position(self) -> int:
        return self._current_position

    @property
    def current_width(self) -> int:
        return self._current_width

    def set_state(self, *, position: int, width: int) -> None:
        """Update the indicator state and reposition within the track."""
        self._current_position = max(position, 0)
        self._current_width = max(width, 0)
        self._indicator.setFixedWidth(self._current_width)
        self._update_layout()

    def resizeEvent(self, a0: Optional[QResizeEvent]) -> None:  # noqa: N802
        super().resizeEvent(a0)
        self._update_layout()

    def _update_layout(self) -> None:
        track_width = self._track_container.width() or DEFAULT_TRACK_WIDTH
        max_position = max(track_width - self._current_width, 0)
        clamped_position = max(0, min(self._current_position, max_position))

        self._left_spacer.setFixedWidth(clamped_position)

        remaining = max(track_width - clamped_position - self._current_width, 0)
        self._right_spacer.setFixedWidth(remaining)


