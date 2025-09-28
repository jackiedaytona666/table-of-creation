"""Scraper for Explore Edmonton's public calendar feed."""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from ..base import Scraper
from ..models import Event
from ..utils import clean_whitespace, parse_datetime

DEFAULT_CALENDAR_URL = (
    "https://www.exploreedmonton.com/api/sitecore/Calendar/DownloadCalendar?language=en&category=all"
)


class ExploreEdmontonScraper(Scraper):
    """Download and parse Explore Edmonton calendar events (ICS feed)."""

    calendar_url = DEFAULT_CALENDAR_URL

    def __init__(self, calendar_url: Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        if calendar_url:
            self.calendar_url = calendar_url

    def fetch_events(self) -> Iterable[Event]:  # pragma: no cover - network
        response = self.get(self.calendar_url)
        events: List[Event] = []
        for raw_event in _parse_ics(response.text):
            title = clean_whitespace(raw_event.get("SUMMARY"))
            if not title:
                continue

            categories = [cat.strip() for cat in raw_event.get("CATEGORIES", "").split(",") if cat.strip()]
            start = parse_datetime(raw_event.get("DTSTART"))
            end = parse_datetime(raw_event.get("DTEND"))
            location = clean_whitespace(raw_event.get("LOCATION"))

            events.append(
                Event(
                    source=self.name,
                    title=title,
                    start=start,
                    end=end,
                    venue=location,
                    address=location,
                    categories=categories,
                    url=clean_whitespace(raw_event.get("URL")),
                    description=clean_whitespace(raw_event.get("DESCRIPTION")),
                    raw=raw_event,
                )
            )

        return events


def _parse_ics(content: str) -> Iterable[Dict[str, str]]:
    """Minimal ICS parser that yields dictionaries for each VEVENT block."""

    if not content:
        return []

    blocks = content.split("BEGIN:VEVENT")
    events: List[Dict[str, str]] = []
    for block in blocks[1:]:
        if "END:VEVENT" not in block:
            continue
        body, _ = block.split("END:VEVENT", 1)
        unfolded = _unfold_lines(body)
        data: Dict[str, str] = {}
        for line in unfolded:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.split(";", 1)[0].strip().upper()
            data[key] = value.strip()
        events.append(data)
    return events


def _unfold_lines(block: str) -> List[str]:
    lines: List[str] = []
    for raw_line in block.strip().splitlines():
        if not raw_line:
            continue
        if raw_line.startswith(" ") and lines:
            lines[-1] += raw_line[1:]
        else:
            lines.append(raw_line)
    return lines
