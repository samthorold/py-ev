import logging
from dataclasses import dataclass

from event_loop import Event

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class MyEv(Event):
    a: str


class Player:
    def __init__(self, *, name: str) -> None:
        self.name = name

    def act(self, event: Event) -> list[Event]:
        logger.debug("Acting on event %r", event)
        if event.t >= 10:
            return []
        return [MyEv(t=event.t + 1, a="b" if (event.t % 2) else "c")]
