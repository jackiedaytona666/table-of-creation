"""Composable pipeline for post-processing events."""
from __future__ import annotations

from typing import Iterable, List, Sequence

from ..models import Event


class PipelineStep:
    """A pipeline step transforms a list of events."""

    def run(self, events: List[Event]) -> List[Event]:  # pragma: no cover - interface
        raise NotImplementedError


class EventPipeline:
    """Run a sequence of processing steps over aggregated events."""

    def __init__(self, steps: Sequence[PipelineStep]):
        self.steps = list(steps)

    def run(self, events: Iterable[Event]) -> List[Event]:
        processed = list(events)
        for step in self.steps:
            processed = step.run(processed)
        return processed
