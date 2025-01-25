import logging
import random
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from itertools import product
from typing import Iterator, Self

logger = logging.getLogger(__name__)


BLACKJACK = 21


class Suit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


class Face(Enum):
    ACE = 1
    DEUCE = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


FACE_VALUES = {
    Face.DEUCE: (2,),
    Face.THREE: (3,),
    Face.FOUR: (4,),
    Face.FIVE: (5,),
    Face.SIX: (6,),
    Face.SEVEN: (7,),
    Face.EIGHT: (8,),
    Face.NINE: (9,),
    Face.TEN: (10,),
    Face.JACK: (10,),
    Face.QUEEN: (10,),
    Face.KING: (10,),
    Face.ACE: (1, 11),
}


class Card:
    def __init__(self, suit: Suit, face: Face):
        self.suit = suit
        self.face = face

    def __repr__(self) -> str:
        return f"{self.suit} {self.face}"


class Deck:
    @classmethod
    def new(cls, decks: int = 6, shuffle: bool = True) -> Self:
        deck = cls(
            [
                Card(suit=suit, face=rank)
                for suit in Suit
                for rank in Face
                for _ in range(decks)
            ]
        )
        deck.shuffle()
        return deck

    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.drawn: list[Card] = []
        self.random = random.Random()

    def __len__(self) -> int:
        return len(self.cards)

    def __repr__(self) -> str:
        return f"Deck (cards {len(self.cards)}, drawn {len(self.drawn)})"

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError("Deck is empty")
        card = self.cards.pop()
        # logger.debug("Drawing card %r", card)
        self.drawn.append(card)
        return card

    def shuffle(self) -> None:
        self.random.shuffle(self.cards)

    def cut(self, idx: int | None = None, shuffle: bool = True) -> None:
        if shuffle:
            self.shuffle()
        idx = self.random.randint(0, len(self.cards)) if idx is None else idx
        logger.debug("Cutting cards %d from %d", idx, len(self.cards))
        left = self.cards[:idx]
        right = self.cards[idx:]
        self.cards = right + left


class Hand:
    def __init__(self, cards: list[Card] | None = None) -> None:
        self.cards = [] if cards is None else cards

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, idx: int) -> Card:
        return self.cards[idx]

    def __repr__(self) -> str:
        return f"<Hand(cards={self.cards})>"

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def values(self) -> list[int]:
        card_values = [FACE_VALUES[card.face] for card in self.cards]
        return [sum(vals) for vals in product(*card_values)]


class Player(ABC):
    def __init__(
        self,
        name: str,
        hands: list[Hand] | None = None,
        id: str | None = None,
    ) -> None:
        self.id = uuid.uuid4().hex if id is None else id
        self.name = name
        self.hands = [Hand()] if hands is None else hands
        self.current_hand_idx = 0

    def __hash__(self) -> int:
        return hash(self.id)

    @abstractmethod
    def hit(self, visible_cards: list[Card], dealer: list[Card]) -> bool: ...

    @property
    def current_hand(self) -> Hand:
        return self.hands[self.current_hand_idx]

    def add_card(self, card: Card) -> None:
        self.hands[self.current_hand_idx].add_card(card)

    def split(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        logger.debug("Player %s splitting hand %r", self.id[-7:], self.current_hand)
        if len(self.current_hand) != 2:
            return False
        if (
            FACE_VALUES[self.current_hand[0].face][0]
            != FACE_VALUES[self.current_hand[1].face][0]
        ):
            return False
        self.hands = [
            Hand(cards=[self.current_hand[0]]),
            Hand(cards=[self.current_hand[1]]),
        ]
        return True


class Dealer(Player):
    def hit(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        values = self.current_hand.values()
        # https://bicyclecards.com/how-to-play/blackjack
        # If the dealer has an ace, and counting it as 11 would bring the total to 17 or more
        # (but not over 21), the dealer must count the ace as 11 and stand
        if any(16 < value <= BLACKJACK for value in values):
            return False
        if all(value > BLACKJACK for value in values):
            return False
        return True

    def split(self, visible_cards: list[Card], dealer: list[Card]) -> bool:
        return False


class Table:
    def __init__(self, deck: Deck, dealer_id: str, player_ids: list[str]) -> None:
        self.deck = deck
        self.player_ids = player_ids
        self.dealer_id = dealer_id
        self.current_player = player_ids[0]
        self.visible_cards: list[Card] = []
        self.dealer_visible_cards: list[Card] = []

    def draw(self, is_visible: bool = True, dealer: bool = False) -> Card:
        card = self.deck.draw()
        if is_visible:
            self.visible_cards.append(card)
            if dealer:
                self.dealer_visible_cards.append(card)
        return card

    def deal(self) -> Iterator[tuple[str, Card]]:
        self.dealer_visible_cards = []
        for player in self.player_ids:
            yield (player, self.draw())
        yield (self.dealer_id, self.draw(dealer=True))
        for player in self.player_ids:
            yield (player, self.draw())
        yield (self.dealer_id, self.draw(is_visible=False))

    def dealer_reveal(self, card: Card) -> None:
        self.dealer_visible_cards.append(card)
