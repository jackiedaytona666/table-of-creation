"""Generic Socrata-powered scraper for City of Edmonton open data events."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Iterable, List, Optional

from ..base import BatchedScraper
from ..models import Event
from ..utils import clean_whitespace, coerce_list, parse_datetime

SOCRATA_DOMAIN = "https://data.edmonton.ca"


class EdmontonSocrataEventsScraper(BatchedScraper):
    """Scrape event-style datasets exposed via the City of Edmonton Socrata API."""

    base_url_template = SOCRATA_DOMAIN + "/resource/{dataset_id}.json"
    max_pages = 5
    page_size = 50

    def __init__(
        self,
        dataset_id: str,
        *,
        app_token: Optional[str] = None,
        field_map: Optional[Dict[str, str]] = None,
        where_clause: Optional[str] = None,
        **kwargs,
    ) -> None:
        if not dataset_id:
            raise ValueError("dataset_id is required for EdmontonSocrataEventsScraper")
        super().__init__(**kwargs)
        self.dataset_id = dataset_id
        self.app_token = app_token
        self.field_map = field_map or DEFAULT_FIELD_MAP.copy()
        self.where_clause = where_clause

    def fetch_page(self, page_number: int) -> Iterable[Event]:  # pragma: no cover - network
        params = {
            "$limit": self.page_size,
            "$offset": (page_number - 1) * self.page_size,
        }

        start_field = self.field_map.get("start")
        if start_field:
            today_iso = datetime.utcnow().date().isoformat()
            clauses = [f"{start_field} >= '{today_iso}'"]
            if self.where_clause:
                clauses.append(self.where_clause)
            params["$where"] = " AND ".join(clauses)
        elif self.where_clause:
            params["$where"] = self.where_clause

        headers = {}
        if self.app_token:
            headers["X-App-Token"] = self.app_token

        url = self.base_url_template.format(dataset_id=self.dataset_id)
        response = self.get(url, params=params, headers=headers)
        payload: List[Dict[str, str]] = response.json()
        events: List[Event] = []
        for item in payload:
            title = clean_whitespace(item.get(self.field_map["title"])) if self.field_map.get("title") else None
            if not title:
                continue

            start = parse_datetime(item.get(self.field_map["start"])) if self.field_map.get("start") else None
            end = parse_datetime(item.get(self.field_map["end"])) if self.field_map.get("end") else None

            latitude = _parse_float(item.get(self.field_map["latitude"])) if self.field_map.get("latitude") else None
            longitude = _parse_float(item.get(self.field_map["longitude"])) if self.field_map.get("longitude") else None

            events.append(
                Event(
                    source=self.name,
                    title=title,
                    start=start,
                    end=end,
                    venue=clean_whitespace(item.get(self.field_map["venue"])) if self.field_map.get("venue") else None,
                    address=clean_whitespace(item.get(self.field_map["address"])) if self.field_map.get("address") else None,
                    latitude=latitude,
                    longitude=longitude,
                    categories=coerce_list(item.get(self.field_map["categories"])) if self.field_map.get("categories") else [],
                    url=clean_whitespace(item.get(self.field_map["url"])) if self.field_map.get("url") else None,
                    cost=clean_whitespace(item.get(self.field_map["cost"])) if self.field_map.get("cost") else None,
                    description=clean_whitespace(item.get(self.field_map["description"]))
                    if self.field_map.get("description")
                    else None,
                    raw=item,
                )
            )

        return events


DEFAULT_FIELD_MAP: Dict[str, Optional[str]] = {
    "title": "event_name",
    "start": "start_date",
    "end": "end_date",
    "venue": "location",
    "address": "address",
    "latitude": "latitude",
    "longitude": "longitude",
    "categories": None,
    "url": "website",
    "cost": "cost",
    "description": "description",
}


def _parse_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
