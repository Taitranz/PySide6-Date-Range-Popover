"""Tests for the time completer utility helpers."""

from __future__ import annotations

import os
from typing import cast

import pytest
from date_range_popover.components.inputs.time_completer import (
    create_time_completer,
    dismiss_time_popup,
    generate_time_options,
    show_time_popup,
)
from date_range_popover.styles.theme import ColorPalette
from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget


def test_generate_time_options_respects_step_bounds() -> None:
    """Steps outside the [1, 60] range should be clamped safely."""

    minute_options = generate_time_options(0)
    assert minute_options[1] == "00:01"
    assert minute_options[-1] == "23:59"

    half_hour_options = generate_time_options(30)
    assert half_hour_options[0:3] == ["00:00", "00:30", "01:00"]
    assert half_hour_options[-1] == "23:30"


def test_create_time_completer_applies_palette_styles(qapp: QApplication) -> None:
    """The completer popup should inherit palette-driven styling."""

    parent = QWidget()
    palette = ColorPalette()
    model = QStringListModel(generate_time_options(15))
    completer = create_time_completer(parent=parent, palette=palette, time_model=model)
    assert completer.maxVisibleItems() == 7
    popup = completer.popup()
    assert popup is not None
    assert palette.time_popup_background in popup.styleSheet()
    assert palette.time_popup_selected_background in popup.styleSheet()


def test_show_and_dismiss_time_popup_toggles_visibility(qapp: QApplication) -> None:
    """The popup helper functions should toggle the completer visibility."""

    if os.environ.get("QT_QPA_PLATFORM", "").lower() == "offscreen":
        pytest.skip("Popup helpers require a platform plugin with window support")

    parent = QWidget()
    parent.show()
    palette = ColorPalette()
    model = QStringListModel(generate_time_options(15))
    completer = create_time_completer(parent=parent, palette=palette, time_model=model)

    line_edit = QLineEdit(parent)
    line_edit.setCompleter(completer)
    line_edit.setText("12:00")

    show_time_popup(line_edit)
    qapp.processEvents()
    popup = completer.popup()
    assert popup is not None
    popup_widget = cast(QWidget, popup)
    assert popup_widget.isVisible()

    # The popup is owned by the completer, so delete the line edit (and
    # parent widget) before tearing down the event loop to avoid spuriously
    # delivering events to a destroyed DateTimeSelector (the plug-in host for
    # these helpers).
    line_edit.deleteLater()
    parent.deleteLater()

    dismiss_time_popup(line_edit)
    qapp.processEvents()
    assert not popup_widget.isVisible()
