"""PyEv Python Discrete Event Loop."""

import logging
import random

from app.config import Config
from app.event_loop import EventLoop, ProcessProtocol
from app.game import Card, Deck, Player, Table
from app.processes import DealerProcess, PlayerProcess

logger = logging.getLogger(__name__)


CONFIG = Config()


logging.basicConfig(level=CONFIG.log_level)


class RandomPlayer(Player):
    def hit(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        return random.random() < 0.5


players: list[Player] = [RandomPlayer(name="p1")]

table = Table(deck=Deck.new(decks=CONFIG.n_decks), players=players)


processes: list[ProcessProtocol] = [
    PlayerProcess(player=player, table=table) for player in players
]
processes.append(DealerProcess(dealer=table.dealer, table=table))

loop = EventLoop(processes=processes)
loop.run()
