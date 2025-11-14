from __future__ import annotations

"""
QSS template helpers shared by calendar widgets.

Qt style sheets end up as large inline strings sprinkled throughout widgets,
which makes it difficult to keep the visual system consistent. These helpers
centralise the common button styles used by the month/year views so themes can
swap palette tokens without editing every widget.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CircularButtonStyle:
    """Parameter bag used by the helper functions below."""

    background: str
    text_color: str
    radius: int


def circular_button_selected_qss(style: CircularButtonStyle) -> str:
    """Return the selected-state stylesheet for circular calendar buttons."""

    return (
        "QPushButton {"
        f"background-color: {style.background};"
        f"color: {style.text_color};"
        "border: none;"
        f"border-radius: {style.radius}px;"
        "padding: 0;"
        "outline: none;"
        "}"
    )


@dataclass(frozen=True, slots=True)
class CircularButtonHoverStyle:
    """Parameters for the hover/default button stylesheet."""

    text_color: str
    hover_background: str
    hover_text_color: str
    radius: int


def circular_button_default_qss(style: CircularButtonHoverStyle) -> str:
    """Return the default-state stylesheet with hover rules."""

    return (
        "QPushButton {"
        "background-color: transparent;"
        f"color: {style.text_color};"
        "border: none;"
        f"border-radius: {style.radius}px;"
        "padding: 0;"
        "outline: none;"
        "}"
        "QPushButton:hover {"
        f"background-color: {style.hover_background};"
        f"color: {style.hover_text_color};"
        "outline: none;"
        "}"
    )


__all__ = [
    "CircularButtonHoverStyle",
    "CircularButtonStyle",
    "circular_button_default_qss",
    "circular_button_selected_qss",
]


