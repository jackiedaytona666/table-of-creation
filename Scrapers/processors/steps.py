"""Reusable pipeline steps for event processing."""
from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from ..models import Event
from ..utils import clean_whitespace
from .pipeline import PipelineStep


class NormalizeTextStep(PipelineStep):
    """Normalize whitespace and basic casing for text fields."""

    text_fields = ("title", "venue", "address", "description", "cost")

    def run(self, events: List[Event]) -> List[Event]:
        for event in events:
            for field_name in self.text_fields:
                value = getattr(event, field_name, None)
                if isinstance(value, str):
                    setattr(event, field_name, clean_whitespace(value))
        return events


class DedupeStep(PipelineStep):
    """Drop duplicate records based on title and start time heuristics."""

    def __init__(self, *, key: Optional[Callable[[Event], Tuple[Optional[str], Optional[str]]]] = None) -> None:
        self.key = key or (lambda event: (event.title.lower() if event.title else None, event.start.isoformat() if event.start else None))

    def run(self, events: List[Event]) -> List[Event]:
        seen: "OrderedDict[Tuple[Optional[str], Optional[str]], Event]" = OrderedDict()
        for event in events:
            dedupe_key = self.key(event)
            if dedupe_key not in seen:
                seen[dedupe_key] = event
        return list(seen.values())


@dataclass
class EnrichGeocodeStep(PipelineStep):
    """Enrich events with latitude/longitude via a pluggable geocoder callable."""

    geocoder: Callable[[Event], Optional[Tuple[float, float]]]
    cache: Dict[str, Tuple[float, float]] = field(default_factory=dict)

    def run(self, events: List[Event]) -> List[Event]:
        for event in events:
            if event.latitude is not None and event.longitude is not None:
                continue
            lookup_key = (event.venue or event.address or "").strip()
            if not lookup_key:
                continue
            if lookup_key in self.cache:
                lat, lon = self.cache[lookup_key]
            else:
                result = self.geocoder(event)
                if not result:
                    continue
                lat, lon = result
                self.cache[lookup_key] = (lat, lon)
            event.latitude = lat
            event.longitude = lon
        return events
