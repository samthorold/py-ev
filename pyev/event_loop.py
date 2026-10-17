"""PyEv Python Discrete Event Loop."""

from collections.abc import Iterable
from typing import Protocol

from pyev.event_queue import Event, EventQueue


class ProcessProtocol[T](Protocol):
    def __call__(self, event: T, t: int) -> Iterable[tuple[T, int]]: ...


class EventLoop[T]:
    def __init__(
        self,
        processes: Iterable[ProcessProtocol[T]] = (),
        timestep: int = 0,
    ) -> None:
        self.current_timestep = timestep
        self.processes = list(processes)
        self.events = EventQueue[T]()

    def add_process(self, process: ProcessProtocol[T]) -> None:
        self.processes.append(process)

    def add_event(self, event: T, t: int) -> None:
        if t < self.current_timestep:
            raise RuntimeError(
                "Cannot add event in the past."
                f" Current timestep: {self.current_timestep}, event timestep: {t}."
            )
        self.events.push(data=event, t=t)

    def _pop_due(self) -> Event[T] | None:
        """Pop the next queued event if it is due at the current timestep."""
        if (item := self.events.peek()) is not None and item.t <= self.current_timestep:
            return self.events.pop()
        return None

    def broadcast(self) -> None:
        while (item := self._pop_due()) is not None:
            for process in self.processes:
                for response_event, response_event_t in process(
                    item.data,
                    self.current_timestep,
                ):
                    self.add_event(response_event, response_event_t)

    def tick(self) -> bool:
        self.broadcast()
        if queue_event := self.events.peek():
            self.current_timestep = queue_event.t
            return True
        return False

    def run(self) -> None:
        while self.tick():
            pass
