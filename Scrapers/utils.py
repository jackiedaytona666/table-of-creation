"""Shared utility helpers for scrapers."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable, Optional

from dateutil import parser as date_parser

ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


def parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse a datetime string into a timezone-aware UTC datetime when possible."""

    if not value:
        return None

    text = value.strip()
    if not text or text in {"TBA", "TBD"}:
        return None

    try:
        dt = date_parser.parse(text)
    except (ValueError, TypeError):
        return None

    if dt.tzinfo is None:
        return dt

    return dt.astimezone(timezone.utc)


def coerce_list(value: Optional[Iterable[str]]) -> list[str]:
    if not value:
        return []
    return [item for item in value if item]


def clean_whitespace(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    collapsed = re.sub(r"\s+", " ", text)
    return collapsed.strip() or None
