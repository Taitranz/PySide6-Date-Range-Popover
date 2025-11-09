from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DateTimeRangeSelector(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(34)
        self.setStyleSheet("background-color: #cfe2f3; border-radius: 0px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = QLabel("component 2", self)
        layout.addWidget(label)

