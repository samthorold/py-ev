import logging
from dataclasses import dataclass

from app.event_loop import Event, LoopStarted
from app.game import Card, Dealer, Player, Table

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
class SplitDecisionRequested(Event):
    player_id: str


@dataclass(kw_only=True, frozen=True)
class CardIssued(Event):
    player_id: str
    card: Card


@dataclass(kw_only=True, frozen=True)
class Split(Event):
    player_id: str


@dataclass(kw_only=True, frozen=True)
class HitDecisionRequested(Event):
    player_id: str


@dataclass(kw_only=True, frozen=True)
class EndTurn(Event):
    player_id: str


class PlayerProcess:
    def __init__(self, *, player: Player, table: Table) -> None:
        self.player = player
        self.table = table

    def __call__(self, event: Event) -> list[Event]:
        # logger.debug("%s acting on event %r", self.__class__.__name__, event)
        match event:
            case CardIssued(player_id=player_id, card=card):
                if self.player.id == player_id:
                    self.player.add_card(card)
                return []
            case SplitDecisionRequested(t=t, player_id=player_id):
                if self.player.id == player_id:
                    if self.player.split(
                        visible_cards=self.table.visible_cards,
                        dealer=self.table.dealer_visible_cards,
                    ):
                        return [Split(t=t + 1, player_id=player_id)]
                return []
            case _:
                return []


class DealerProcess:
    def __init__(self, *, dealer: Dealer, table: Table) -> None:
        self.dealer = dealer
        self.table = table

    def __call__(self, event: Event) -> list[Event]:
        # logger.debug("%s acting on event %r", self.__class__.__name__, event)
        match event:
            case LoopStarted(t=t):
                return [NewPlay(t=t + 1)]
            case NewPlay(t=t):
                events: list[Event] = [
                    CardIssued(t=t + 1, player_id=player_id, card=card)
                    for player_id, card in self.table.deal()
                ]
                events.append(
                    SplitDecisionRequested(t=t + 1, player_id=self.table.current_player)
                )
                return events
            case _:
                return []
