"""PyEv Python Discrete Event Loop."""

import logging
import os
import random

from event_loop import EventLoop, ProcessProtocol
from game import Card, Deck, Player, Table
from processes import DealerProcess, PlayerProcess


logger = logging.getLogger(__name__)


logging.basicConfig(level=os.environ.get("PYEV_LOG_LEVEL") or logging.DEBUG)


class RandomPlayer(Player):
    def hit(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        return random.random() < 0.5


players: list[Player] = [RandomPlayer(name="p1")]

table = Table(deck=Deck.new(), players=players)


processes: list[ProcessProtocol] = [
    PlayerProcess(player=player, table=table) for player in players
]
processes.append(DealerProcess(dealer=table.dealer, table=table))

loop = EventLoop(processes=processes)
loop.run()
