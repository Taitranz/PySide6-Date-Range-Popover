"""Button strip that exposes signals for selecting a date range."""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from ..styles.constants import (
    BUTTON_CONTAINER_BACKGROUND,
    BUTTON_GAP,
    BUTTON_STRIP_BOTTOM_MARGIN,
    CUSTOM_RANGE_BUTTON_WIDTH,
    DATE_BUTTON_WIDTH,
)
from ..styles.constants import create_button_font


class ButtonStrip(QWidget):
    """Displays Date and Custom Range buttons."""

    date_selected = pyqtSignal()
    custom_range_selected = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {BUTTON_CONTAINER_BACKGROUND};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, BUTTON_STRIP_BOTTOM_MARGIN)
        layout.setSpacing(0)

        self.date_button = QPushButton("Date", self)
        self.date_button.setFont(create_button_font())
        self.date_button.setFixedWidth(DATE_BUTTON_WIDTH)
        self.date_button.setMinimumHeight(0)
        self.date_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.date_button.setStyleSheet("text-align: left; padding: 0; margin: 0; border: none; outline: none;")

        self.custom_range_button = QPushButton("Custom range", self)
        self.custom_range_button.setFont(create_button_font())
        self.custom_range_button.setFixedWidth(CUSTOM_RANGE_BUTTON_WIDTH)
        self.custom_range_button.setMinimumHeight(0)
        self.custom_range_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.custom_range_button.setStyleSheet("text-align: left; padding: 0; margin: 0; border: none; outline: none;")

        layout.addWidget(
            self.date_button,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
        )

        gap = QWidget(self)
        gap.setFixedWidth(BUTTON_GAP)
        layout.addWidget(gap)

        layout.addWidget(
            self.custom_range_button,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
        )
        layout.addStretch()

        self.date_button.clicked.connect(self.date_selected.emit)  # type: ignore[attr-defined]
        self.custom_range_button.clicked.connect(self.custom_range_selected.emit)  # type: ignore[attr-defined]


