from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget

from ...styles.theme import ColorPalette


class DraggableHeaderStrip(QWidget):
    """Custom header widget that can be dragged to move its top-level parent."""

    def __init__(
        self,
        parent_widget: QWidget,
        *,
        palette: ColorPalette | None = None,
    ) -> None:
        super().__init__(parent_widget)
        self._parent_widget = parent_widget
        self._drag_position = QPoint()
        self._palette = palette or ColorPalette()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.apply_palette(self._palette)

    def apply_palette(self, palette: ColorPalette) -> None:
        self._palette = palette
        self.setStyleSheet(f"background-color: {palette.header_background}; border-radius: 0px;")

    def mousePressEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event and event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self._parent_widget.pos()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event and event.buttons() == Qt.MouseButton.LeftButton:
            self._parent_widget.move(event.globalPosition().toPoint() - self._drag_position)


__all__ = ["DraggableHeaderStrip"]
