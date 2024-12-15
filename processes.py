import logging
from dataclasses import dataclass

from event_loop import Event

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class NewPlay(Event):
    """
    - Deal card face-up to players left to right then to dealer
    - Deal card face-up to players left to right then face-down to dealer
    - If dealer's face-up card to 10 or ace, they check their face-down card
    - If the face-down card makes a natural, (do something).
    """


class PlayerProcess:
    def __init__(self, *, name: str) -> None:
        self.name = name

    def act(self, event: Event) -> list[Event]:
        logger.debug("%s acting on event %r", self.__class__.__name__, event)
        return []


class HouseProcess:
    def act(self, event: Event) -> list[Event]:
        logger.debug("%s acting on event %r", self.__class__.__name__, event)
        return []
