import pytest

from app.game import Card, Dealer, Face, Hand, Suit


@pytest.mark.parametrize(
    "hand,expected",
    [
        # blackjack
        (
            Hand(
                cards=[
                    Card(suit=Suit.CLUBS, face=Face.ACE),
                    Card(suit=Suit.CLUBS, face=Face.TEN),
                ]
            ),
            False,
        ),
        # < 17
        (
            Hand(
                cards=[
                    Card(suit=Suit.CLUBS, face=Face.SIX),
                    Card(suit=Suit.CLUBS, face=Face.TEN),
                ]
            ),
            True,
        ),
        # == 17
        (
            Hand(
                cards=[
                    Card(suit=Suit.CLUBS, face=Face.SEVEN),
                    Card(suit=Suit.CLUBS, face=Face.TEN),
                ]
            ),
            False,
        ),
        # bust
        (
            Hand(
                cards=[
                    Card(suit=Suit.CLUBS, face=Face.SIX),
                    Card(suit=Suit.CLUBS, face=Face.TEN),
                    Card(suit=Suit.CLUBS, face=Face.TEN),
                ]
            ),
            False,
        ),
    ],
)
def test_dealer__hit(hand: Hand, expected: bool) -> None:
    dealer = Dealer(name="Dealer", hands=[hand])
    assert dealer.hit(visible_cards=[], dealer=[]) == expected
