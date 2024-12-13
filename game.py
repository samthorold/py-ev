from enum import Enum
import random


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


class Card:
    def __init__(self, suit: Suit, face: Face):
        self.suit = suit
        self.face = face

    def __repr__(self) -> str:
        return f"{self.suit} {self.face}"


class Deck:
    @classmethod
    def new(cls, decks: int = 1, shuffle: bool = True):
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
        self.drawn.append(card)
        return card

    def shuffle(self) -> None:
        self.random.shuffle(self.cards)

    def cut(self, idx: int | None = None, shuffle: bool = True) -> None:
        if shuffle:
            self.shuffle()
        idx = self.random.randint(0, len(self.cards)) if idx is None else idx
        left = self.cards[:idx]
        right = self.cards[idx:]
        self.cards = right + left
