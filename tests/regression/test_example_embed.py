"""Regression tests that mirror the README/basic demo setup."""

from __future__ import annotations

import os

from pytestqt.qtbot import QtBot

from date_range_popover import DatePickerConfig, DateRangePopover, PickerMode


def test_basic_popover_demo_configuration(qtbot: QtBot) -> None:
    """
    The configuration showcased in README/examples should construct cleanly.

    This acts as a smoke test for the public embed surface: if wiring changes
    break the default `DatePickerConfig` or the widget cannot be created in a
    headless environment, this test will fail early.
    """

    popover = DateRangePopover(config=DatePickerConfig(mode=PickerMode.DATE))
    qtbot.addWidget(popover)

    if os.environ.get("QT_QPA_PLATFORM", "").lower() != "offscreen":
        # A short show/hide cycle ensures paint paths keep working when a real
        # widget backend is available. Some CI environments rely on the
        # ``offscreen`` platform plugin, which crashes when ``show()`` is
        # invoked, so we skip the visibility assertions in that case.
        popover.show()
        assert popover.isVisible()

    popover.cleanup()
