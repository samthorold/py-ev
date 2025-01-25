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
        """Represents a discrete event loop.

        Args:
            processes: A list of processes that will be executed in the event loop.
            events: A sequence of events to be added to the event loop.
            current_timestep: The current timestep of the event loop.
            add_loop_started_event: Whether to add a LoopStarted event to the event loop.

        Examples:
            >>> from app.event_loop import EventLoop, Event, LoopStarted
            >>> class Process:
            ...     def act(self, event: Event) -> Sequence[Event]:
            ...         if isinstance(event, LoopStarted):
            ...             return [Event(t=1), Event(t=2)]
            ...         return []
            ...
            >>> processes = [Process()]
            >>> events = [Event(t=0)]
            >>> event_loop = EventLoop(processes, events)
            >>> event_loop.run()
        """
        self.processes = processes
        self.events: deque[Event] = deque()
        if add_loop_started_event:
            self.add_event(LoopStarted(t=0))
        for event in events or []:
            self.add_event(event)
        self.current_timestep = current_timestep

    def add_event(self, event: Event) -> None:
        """Adds an event to the event loop.

        Args:
            event: The event to add to the event loop.

        Examples:
            >>> from app.event_loop import EventLoop, Event
            >>> event_loop = EventLoop(processes=[])
            >>> event_loop.add_event(Event(t=0))
        """
        logger.debug("Adding event %r", event)
        self.events.insert(event.t + 1, event)

    def peek_event(self) -> Event | None:
        """Returns the next event without removing it from the backlog."""
        if len(self.events) > 0:
            return self.events[0]
        return None

    def next_event(self) -> Event | None:
        """Returns the next event and removes it from the backlog."""
        if event := self.peek_event():
            if event.t > self.current_timestep:
                return None
            return self.events.popleft()
        return None

    def tick(self) -> bool:
        """Broadcasts all events for the current timestep to all processes."""
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
        """Runs the event loop until there are no more events."""
        while self.tick():
            pass
