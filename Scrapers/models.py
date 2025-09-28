"""Data models used across scrapers and processors."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Event:
    """Normalized representation of a person-attracting event."""

    source: str
    title: str
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    venue: Optional[str] = None
    address: Optional[str] = None
    city: str = "Edmonton"
    province: str = "AB"
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    categories: List[str] = field(default_factory=list)
    url: Optional[str] = None
    cost: Optional[str] = None
    description: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the event to a JSON-friendly dictionary."""

        return {
            "source": self.source,
            "title": self.title,
            "start": self.start.isoformat() if self.start else None,
            "end": self.end.isoformat() if self.end else None,
            "venue": self.venue,
            "address": self.address,
            "city": self.city,
            "province": self.province,
            "postal_code": self.postal_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "categories": self.categories,
            "url": self.url,
            "cost": self.cost,
            "description": self.description,
            "raw": self.raw,
        }


@dataclass
class ScrapeResult:
    """Wrapper for results and metadata from a scraper run."""

    events: List[Event]
    fetched_at: datetime
    source: str
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the scrape result."""

        return {
            "source": self.source,
            "fetched_at": self.fetched_at.isoformat(),
            "events": [event.to_dict() for event in self.events],
            "errors": self.errors,
        }
