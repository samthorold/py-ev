"""PyEv Python Discrete Event Loop."""

import logging
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Protocol, Sequence

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class Event:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    t: int


@dataclass(kw_only=True, frozen=True)
class LoopStarted(Event):
    pass


class ProcessProtocol(Protocol):
    def act(self, event: Event) -> Sequence[Event]: ...


class EventLoop:
    def __init__(
        self,
        processes: list[ProcessProtocol],
        events: Sequence[Event] | None = None,
        current_timestep: int = 0,
        add_loop_started_event: bool = True,
    ) -> None:
        self.processes = processes
        self.events: deque[Event] = deque()
        if add_loop_started_event:
            self.add_event(LoopStarted(t=0))
        for event in events or []:
            self.add_event(event)
        self.current_timestep = current_timestep

    def add_event(self, event: Event) -> None:
        logger.debug("Adding event %r", event)
        self.events.insert(event.t + 1, event)

    def peek_event(self) -> Event | None:
        if len(self.events) > 0:
            return self.events[0]

    def next_event(self) -> Event | None:
        if event := self.peek_event():
            if event.t > self.current_timestep:
                return None
            return self.events.popleft()

    def tick(self) -> bool:
        logger.debug("Ticking at %d", self.current_timestep)
        while event := self.next_event():
            logger.debug("Broadcasting event %r", event)
            for process in self.processes:
                for event in process.act(event):
                    self.add_event(event)
        if event := self.peek_event():
            self.current_timestep = event.t
            return True
        logger.debug("No events to process")
        return False

    def run(self) -> None:
        while self.tick():
            pass
