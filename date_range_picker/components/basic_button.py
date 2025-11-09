from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QSizePolicy, QWidget

from ..styles import constants


class BasicButton(QPushButton):
    """Simple styled action button without click behaviour."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        label: str = "Done",
        width: int | None = None,
        height: int | None = None,
        background_color: str | None = None,
        hover_background_color: str | None = None,
        pressed_background_color: str | None = None,
        border_color: str | None = None,
        font_color: str | None = None,
        hover_font_color: str | None = None,
        pressed_font_color: str | None = None,
    ) -> None:
        super().__init__(label, parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(constants.create_button_font())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._background_color = background_color or constants.ACTION_BUTTON_BACKGROUND
        self._hover_background_color = (
            hover_background_color or constants.ACTION_BUTTON_HOVER_BACKGROUND
        )
        self._pressed_background_color = (
            pressed_background_color or constants.ACTION_BUTTON_PRESSED_BACKGROUND
        )
        self._border_color = border_color or constants.TRACK_BACKGROUND
        self._font_color = font_color or constants.BUTTON_SELECTED_COLOR
        self._hover_font_color = hover_font_color or self._font_color
        self._pressed_font_color = pressed_font_color or self._hover_font_color

        if width is None:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        else:
            self.setFixedWidth(width)
            self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        final_height = height if height is not None else constants.ACTION_BUTTON_HEIGHT
        self.setFixedHeight(final_height)

        vertical_padding = self._compute_vertical_padding(final_height)
        self._apply_style(vertical_padding)

    def _compute_vertical_padding(self, final_height: int) -> int:
        font_height = self.fontMetrics().height()
        available_space = max(0, final_height - font_height)
        max_padding = constants.ACTION_BUTTON_VERTICAL_PADDING
        computed_padding = available_space // 2
        return min(max_padding, computed_padding)

    def _apply_style(self, vertical_padding: int) -> None:
        self.setStyleSheet(
            (
                "QPushButton {"
                f"background-color: {self._background_color};"
                f"color: {self._font_color};"
                f"border: 1px solid {self._border_color};"
                f"border-radius: {constants.WINDOW_RADIUS}px;"
                f"padding: {vertical_padding}px 0;"
                "}"
                "QPushButton:hover {"
                f"background-color: {self._hover_background_color};"
                f"color: {self._hover_font_color};"
                "}"
                "QPushButton:pressed {"
                f"background-color: {self._pressed_background_color};"
                f"color: {self._pressed_font_color};"
                "}"
                "QPushButton:focus {"
                f"border: 1px solid {constants.BUTTON_SELECTED_COLOR};"
                "}"
            )
        )

