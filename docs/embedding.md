<!-- Embedding & Input Sanitisation Guide -->
# Embedding & Input Sanitisation

`DateRangePopover` is designed to live inside larger desktop apps, which
often means configuration data originates outside of your direct control
(settings files, remote APIs, user-editable forms, etc.). This guide
explains how to safely bridge that external input into the picker.

## 1. Normalise external data

Always convert raw inputs into concrete Python types before building a
`DatePickerConfig`. For example, parse ISO date strings into `QDate`
objects and clamp integers to sensible ranges.

```python
from PyQt6.QtCore import QDate

def parse_iso_date(value: str | None) -> QDate | None:
    if not value:
        return None
    candidate = QDate.fromString(value, "yyyy-MM-dd")
    return candidate if candidate.isValid() else None
```

## 2. Reuse the built-in validators

After you have provisional types, call the validation helpers shipped
with the library to double check everything. They raise descriptive
exceptions you can surface to users or logs.

```python
from date_range_popover.validation import validate_date_range, validate_qdate

def sanitise_payload(payload: dict) -> tuple[QDate | None, QDate | None]:
    start = parse_iso_date(payload.get("start"))
    end = parse_iso_date(payload.get("end"))
    return validate_date_range(start, end, field_name="user_payload")

def sanitise_anchor(date_str: str | None) -> QDate | None:
    return validate_qdate(parse_iso_date(date_str), field_name="anchor", allow_none=True)
```

## 3. Construct `DatePickerConfig` inside `try` / `except`

Wrap config construction so you can gracefully fallback if someone
hands you a bad payload. `DatePickerConfig` re-validates everything in
`__post_init__`, so even if the embedding code misses something you'll
get a deterministic exception.

```python
from date_range_popover import DatePickerConfig, DateRange, PickerMode

def build_config(raw: dict) -> DatePickerConfig:
    range_start, range_end = sanitise_payload(raw.get("range", {}))
    try:
        return DatePickerConfig(
            mode=PickerMode[raw.get("mode", "DATE").upper()],
            initial_range=DateRange(start_date=range_start, end_date=range_end),
            min_date=sanitise_anchor(raw.get("min")),
            max_date=sanitise_anchor(raw.get("max")),
            width=int(raw.get("width", 302)),
            height=int(raw.get("height", 580)),
        )
    except (ValueError, KeyError, Exception) as exc:
        # Map to your own error reporting; fall back to safe defaults.
        raise RuntimeError("Invalid picker configuration") from exc
```

## 4. Handle runtime validation failures

The picker emits strong types (e.g. `DateRange` instances) and its state
manager clamps selections to the configured bounds. If you still need to
double-check at the edge of your system, reuse the validators:

```python
def on_range_selected(date_range: DateRange) -> None:
    start, end = validate_date_range(
        date_range.start_date,
        date_range.end_date,
        field_name="range_selected_signal",
        allow_partial=False,
    )
    persist_selection(start, end)
```

## 5. Clean up embedded widgets

If you dynamically create/destroy popovers, call `DateRangePicker.cleanup`
when you remove them. This stops animations and releases Qt objects so
subsequent embeddings start from a clean slate.

```python
popover = DateRangePopover(config=build_config(payload))
popover.destroyed.connect(popover.cleanup)
```

## 6. Read selection state via properties

The public API exposes `selected_date` and `selected_range` properties
(instead of `get_*` methods). Properties make it trivial to inspect the
current state when wiring menus or command handlers:

```python
if popover.selected_range.end_date is not None:
    print("Range locked in:", popover.selected_range)
```

Refer back to `README.md` for high-level usage and the demo under
`examples/basic_popover_demo.py` for a runnable reference implementation.

