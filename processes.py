import logging
from dataclasses import dataclass

from event_loop import Event
from game import Dealer, Player, Table

logger = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
class NewPlay(Event):
    """
    Game mechanics:

    - Deal card face-up to players left to right then to dealer
    - Deal card face-up to players left to right then face-down to dealer
    - If dealer's face-up card to 10 or ace, they check their face-down card
    - If the face-down card makes a natural, (do something).
    - Left to right, players hit until they are bust or are happy with their hand

    Player turn mechanics:
    - May split
    - For each hand, hit until bust or happy
    """


@dataclass(kw_only=True, frozen=True)
class AskSplit(Event):
    player_id: str


@dataclass(kw_only=True, frozen=True)
class Split(Event):
    player_id: str


class PlayerProcess:
    def __init__(self, *, player: Player, table: Table) -> None:
        self.player = player
        self.table = table

    def act(self, event: Event) -> list[Event]:
        logger.debug("%s acting on event %r", self.__class__.__name__, event)
        return []


class DealerProcess:
    def __init__(self, *, dealer: Dealer, table: Table) -> None:
        self.dealer = dealer
        self.table = table

    def act(self, event: Event) -> list[Event]:
        logger.debug("%s acting on event %r", self.__class__.__name__, event)
        match event:
            case NewPlay(t=t):
                self.table.deal()
                return [AskSplit(t=t + 1, player_id=self.table.current_player.id)]
            case _:
                return []
