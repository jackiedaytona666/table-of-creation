"""Scraper for Eventbrite listings in Edmonton."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Optional

from bs4 import BeautifulSoup

from ..base import BatchedScraper
from ..models import Event
from ..utils import clean_whitespace, parse_datetime

EVENTBRITE_BASE = "https://www.eventbrite.ca"
LISTING_URL = EVENTBRITE_BASE + "/d/canada--edmonton/events/"


class EventbriteEdmontonScraper(BatchedScraper):
    """Scrape the public Eventbrite listings for Edmonton."""

    base_url = LISTING_URL
    max_pages = 3  # Eventbrite paginates heavily; keep the first few pages for freshness.

    def fetch_page(self, page_number: int) -> Iterable[Event]:  # pragma: no cover - network
        params = {"page": page_number}
        response = self.get(self.base_url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select('[data-testid="event-card"]') or soup.select('[data-spec="event-card__content"]')
        events: List[Event] = []
        for card in cards:
            title = clean_whitespace(_text_or_none(card.select_one('[data-spec="event-card__formatted-name"]')))
            if not title:
                continue

            url = _href_or_none(card.select_one("a"))
            if url and url.startswith("/"):
                url = EVENTBRITE_BASE + url

            date_text = clean_whitespace(
                _text_or_none(card.select_one('[data-spec="event-card__date"]') or card.select_one("time"))
            )
            start = _parse_eventbrite_date(date_text)

            venue = clean_whitespace(
                _text_or_none(card.select_one('[data-spec="event-card__sub-event-venue"]'))
            )

            cost = clean_whitespace(_text_or_none(card.select_one('[data-spec="event-card__price"]')))

            events.append(
                Event(
                    source=self.name,
                    title=title,
                    start=start,
                    venue=venue,
                    address="Edmonton, AB",
                    categories=[],
                    url=url,
                    cost=cost,
                    raw={"date_text": date_text},
                )
            )

        return events


def _text_or_none(element: Optional[object]) -> Optional[str]:
    if element is None:
        return None
    get_text = getattr(element, "get_text", None)
    if callable(get_text):
        return get_text(strip=True)
    return None


def _href_or_none(element: Optional[object]) -> Optional[str]:
    if element is None:
        return None
    get_attr = getattr(element, "get", None)
    if callable(get_attr):
        return get_attr("href")
    return None


def _parse_eventbrite_date(text: Optional[str]) -> Optional[datetime]:
    if not text:
        return None

    cleaned = text.replace("–", "-")
    parts = cleaned.split("-")
    if not parts:
        return parse_datetime(cleaned)

    return parse_datetime(parts[0])
