"""Shared outreach helpers — subscriber parsing and targeting criteria."""

from __future__ import annotations

import re

TARGET_SUB_MIN = 5_000
TARGET_SUB_MAX = 100_000


def parse_subscribers(value) -> int | None:
    """Parse subscriber counts from ints, floats, or strings like '12K' / '1.2M'."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)

    text = str(value).strip().lower().replace(",", "")
    if not text:
        return None

    match = re.match(r"^([\d.]+)\s*([km])?$", text)
    if not match:
        digits = re.sub(r"[^\d]", "", text)
        return int(digits) if digits else None

    number = float(match.group(1))
    suffix = match.group(2)
    if suffix == "k":
        number *= 1_000
    elif suffix == "m":
        number *= 1_000_000
    return int(number)


def in_target_range(value) -> bool | None:
    """True if subscribers are within 5k–100k; None if unknown."""
    count = parse_subscribers(value)
    if count is None:
        return None
    return TARGET_SUB_MIN <= count <= TARGET_SUB_MAX


def subscriber_count(creator: dict) -> int | None:
    """Read subscriber count from either outreach list field name."""
    raw = creator.get("subscribers")
    if raw in (None, ""):
        raw = creator.get("subscribers_or_audience")
    return parse_subscribers(raw)