"""PyEv Python Discrete Event Loop."""

import heapq
import logging
from dataclasses import dataclass
from typing import Any, Iterable, Protocol

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class Event:
    pass


@dataclass(kw_only=True, frozen=True)
class _Event:
    t: int
    priority: int
    event: Event

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, _Event):
            return (self.t, self.priority) > (other.t, other.priority)
        raise TypeError(f"Cannot compare Event to {other.__class__}).")


@dataclass(kw_only=True, frozen=True)
class LoopStarted(Event):
    pass


class ProcessProtocol(Protocol):
    def __call__(self, event: Event, t: int) -> Iterable[tuple[Event, int]]: ...


class EventLoop:
    def __init__(self, processes: list[ProcessProtocol], timestep: int = 0) -> None:
        self.current_timestep = timestep
        self.timestamp_event_count: dict[int, int] = {}
        self.processes = processes
        self.events: list[_Event] = []
        self.add_event(LoopStarted(), timestep)

    def add_event(self, event: Event, t: int) -> None:
        if t < self.current_timestep:
            raise RuntimeError(
                "Cannot add event in the past."
                f" Current timestep: {self.current_timestep}, event timestep: {t}."
            )
        count = self.timestamp_event_count.get(t, 0)
        logger.debug("Adding event (t=%d, priority=%d) %r", t, count, event)
        heapq.heappush(self.events, _Event(t=t, priority=count, event=event))
        self.timestamp_event_count[t] = count + 1

    def peek_event(self) -> _Event | None:
        if len(self.events) > 0:
            return self.events[0]
        return None

    def next_event(self) -> _Event | None:
        if (event := self.peek_event()) and event.t <= self.current_timestep:
            return heapq.heappop(self.events)
        return None

    def tick(self) -> bool:
        logger.debug("Ticking at %d", self.current_timestep)
        while event := self.next_event():
            for process in self.processes:
                for response_event, response_event_t in process(event.event, event.t):
                    self.add_event(response_event, response_event_t)
        if event := self.peek_event():
            self.current_timestep = event.t
            return True
        logger.debug("Exhausted events.")
        return False

    def run(self) -> None:
        while self.tick():
            pass
