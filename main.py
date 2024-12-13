"""PyEv Python Discrete Event Loop."""


from collections import deque
from dataclasses import dataclass
import logging
from typing import Protocol


logger = logging.getLogger(__name__)


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


if __name__ == "__main__":

    import os

    logging.basicConfig(level=os.environ.get("PYEV_LOG_LEVEL") or logging.DEBUG)

    @dataclass(kw_only=True, frozen=True)
    class MyEv(Event):
        a: str

    class Process:
        def act(self, event: Event) -> list[Event]:
            logger.debug("Acting on event %r", event)
            if event.t >= 10:
                return []
            return [
                MyEv(t=event.t + 1, a="b" if (event.t % 2) else "c")
            ]

    loop = EventLoop(
        processes=[Process()],
        events=[
            MyEv(t=1, a="a"),
        ],
    )
    loop.run()
