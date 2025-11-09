"""Draggable header strip that allows moving the parent widget."""

from __future__ import annotations

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget

from ..styles.constants import HEADER_BACKGROUND


class DraggableHeaderStrip(QWidget):
    """Custom header widget that can be dragged to move its top-level parent."""

    def __init__(self, parent_widget: QWidget) -> None:
        super().__init__(parent_widget)
        self._parent_widget = parent_widget
        self._drag_position = QPoint()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {HEADER_BACKGROUND}; border-radius: 0px;")

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:  # noqa: N802
        if a0 and a0.button() == Qt.MouseButton.LeftButton:
            self._drag_position = a0.globalPosition().toPoint() - self._parent_widget.pos()

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:  # noqa: N802
        if a0 and a0.buttons() == Qt.MouseButton.LeftButton:
            self._parent_widget.move(a0.globalPosition().toPoint() - self._drag_position)


