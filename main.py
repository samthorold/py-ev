"""PyEv Python Discrete Event Loop."""

import logging
import random

from app.config import Config
from app.game import Card, Dealer, Deck, Player, Table
from app.processes import DealerProcess, Event, NewPlay, PlayerProcess
from pyev.event_loop import EventLoop

logger = logging.getLogger(__name__)


CONFIG = Config()


logging.basicConfig(level=CONFIG.log_level)


class RandomPlayer(Player):
    def hit(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        return random.random() < 0.5


players: list[Player] = [RandomPlayer(id="p", name="p1")]
dealer = Dealer(id="d", name="dealer")

table = Table(
    deck=Deck.new(decks=CONFIG.n_decks),
    dealer_id=dealer.id,
    player_ids=[player.id for player in players],
)

loop = EventLoop[Event]()
loop.add_process(DealerProcess(dealer=dealer, table=table))
for player in players:
    loop.add_process(PlayerProcess(player=player, table=table))

loop.add_event(NewPlay(), 0)
loop.run()
