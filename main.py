"""PyEv Python Discrete Event Loop."""

from dataclasses import dataclass
from event_loop import Event, EventLoop
import logging


logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class MyEv(Event):
    a: str


class Process:
    def act(self, event: Event) -> list[Event]:
        logger.debug("Acting on event %r", event)
        if event.t >= 10:
            return []
        return [MyEv(t=event.t + 1, a="b" if (event.t % 2) else "c")]


if __name__ == "__main__":

    import os

    logging.basicConfig(level=os.environ.get("PYEV_LOG_LEVEL") or logging.DEBUG)

    loop = EventLoop(
        processes=[Process()],
        events=[
            MyEv(t=1, a="a"),
        ],
    )
    loop.run()
