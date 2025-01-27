"""PyEv Python Discrete Event Loop."""

import logging
from typing import Generic, Iterable, Protocol, TypeVar

from pyev.event_queue import EventQueue

logger = logging.getLogger(__name__)


T = TypeVar("T")


class ProcessProtocol(Protocol, Generic[T]):
    def __call__(self, event: T, t: int) -> Iterable[tuple[T, int]]: ...


class EventLoop(Generic[T]):
    def __init__(self, processes: list[ProcessProtocol[T]], timestep: int = 0) -> None:
        self.current_timestep = timestep
        self.processes = processes
        self.events = EventQueue[T]()

    def add_event(self, event: T, t: int) -> None:
        if t < self.current_timestep:
            raise RuntimeError(
                "Cannot add event in the past."
                f" Current timestep: {self.current_timestep}, event timestep: {t}."
            )
        logger.debug("Adding event (t=%d) %r", t, event)
        self.events.push(data=event, t=t)

    def next_event(self) -> T | None:
        if (event := self.events.peek()) and event.t <= self.current_timestep:
            return self.events.pop().data
        return None

    def tick(self) -> bool:
        logger.debug("Ticking at %d", self.current_timestep)
        while event := self.next_event():
            for process in self.processes:
                for response_event, response_event_t in process(
                    event,
                    self.current_timestep,
                ):
                    self.add_event(response_event, response_event_t)
        if queue_event := self.events.peek():
            self.current_timestep = queue_event.t
            return True
        logger.debug("Exhausted events.")
        return False

    def run(self) -> None:
        while self.tick():
            pass
