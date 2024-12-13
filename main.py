"""PyEv Python Discrete Event Loop."""


from collections import deque
from dataclasses import dataclass

from typing import Protocol


@dataclass(kw_only=True, frozen=True)
class Event:
    t: int


class ProcessProtocol(Protocol):
    def act(self, event: Event) -> list[Event]:
        ...


class EventLoop:
    def __init__(
        self,
        processes: list[ProcessProtocol],
        events: list[Event] | None = None,
        current_timestep: int = 0,
    ) -> None:
        self.processes = processes
        self.events: deque[Event] = deque()
        for event in events or []:
            self.add_event(event)
        self.current_timestep = current_timestep

    def add_event(self, event: Event) -> None:
        self.events.insert(event.t + 1, event)

    def peek_event(self) -> Event | None:
        if len(self.events) > 0:
            return self.events[0]

    def next_event(self) -> Event | None:
        if event := self.peek_event():
            if event.t > self.current_timestep:
                return None
            return self.events.popleft()

    def tick(self) -> None:
        while event := self.next_event():
            for process in self.processes:
                for event in process.act(event):
                    self.add_event(event)
        if event := self.peek_event():
            self.current_timestep = event.t
