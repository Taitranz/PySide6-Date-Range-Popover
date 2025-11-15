# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Codecov uploads in CI with a live coverage badge in the README.
- Additional picker mode regression tests covering multi-hop transitions.
- Expanded invalid configuration tests for dimensions, theme payloads, and time steps.

### Changed
- Migrated the entire widget stack from PyQt6 to PySide6, updating imports, signals,
  examples, and documentation to the new binding.

### Fixed
- Tightened theme validation to ensure invalid mapping payloads bubble up with clear errors.
- Pinned the runtime dependency to `PySide6>=6.5,<6.8` until newer wheels are vetted
  across platforms.

### Tests
- Broadened property/edge-case coverage for `DatePickerConfig`, `Theme`, and core validators.
- CI matrix now targets PySide6 6.5.x through 6.7.x.
- Removed the `PyQt6-Qt6-OpenGL` reinstall step in CI; PySide6 wheels already package the needed bits.
- Regression tests skip the popover `show()` cycle when ``QT_QPA_PLATFORM=offscreen`` to avoid headless crashes while still exercising the behavior locally.
- Re-enabled the latest PySide6 wheels (6.7.1+) now that the upstream Qt symbol issue is fixed.
- Added unit tests for date utilities, logging helpers, signal adapters, styles, and picker config/state code to push the tracked package coverage to 100%.

## [0.1.0] - 2024-06-01

### Added
- Initial public release of the PyQt6 date range popover, including the picker widgets,
  state manager, theming system, and demo application.


