"""Base classes and helpers for scrapers."""
from __future__ import annotations

import abc
import logging
from datetime import datetime
from typing import Iterable, List, Optional

import requests
from requests import Response

from .models import Event, ScrapeResult

LOGGER = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 15


class Scraper(abc.ABC):
    """Abstract base class for all scrapers."""

    base_url: Optional[str] = None

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.setdefault(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        )

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def run(self) -> ScrapeResult:
        """Run the scraper and return normalized events with metadata."""

        LOGGER.info("Running %s", self.name)
        fetched_at = datetime.utcnow()
        events: List[Event] = []
        errors: List[str] = []

        try:
            for event in self.fetch_events():
                events.append(event)
        except Exception as exc:  # pragma: no cover - defensive catch
            error_message = f"{self.name} failed: {exc}"
            LOGGER.exception(error_message)
            errors.append(error_message)

        return ScrapeResult(events=events, fetched_at=fetched_at, source=self.name, errors=errors)

    @abc.abstractmethod
    def fetch_events(self) -> Iterable[Event]:
        """Yield normalized events."""

    # Helper methods -----------------------------------------------------

    def get(self, url: str, *, timeout: int = DEFAULT_TIMEOUT, **kwargs) -> Response:
        """Perform a GET request with sane defaults and error logging."""

        LOGGER.debug("GET %s", url)
        response = self.session.get(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, *, timeout: int = DEFAULT_TIMEOUT, **kwargs) -> Response:
        """Perform a POST request with sane defaults and error logging."""

        LOGGER.debug("POST %s", url)
        response = self.session.post(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response


class BatchedScraper(Scraper):
    """Scraper that handles pagination in discrete batches."""

    max_pages: int = 5
    page_size: int = 50

    @abc.abstractmethod
    def fetch_page(self, page_number: int) -> Iterable[Event]:
        """Grab events for a specific page. Should return empty iterator when done."""

    def fetch_events(self) -> Iterable[Event]:
        for page_number in range(1, self.max_pages + 1):
            page_events = list(self.fetch_page(page_number))
            if not page_events:
                LOGGER.debug("No events returned for %s page %s; stopping", self.name, page_number)
                break
            for event in page_events:
                yield event
