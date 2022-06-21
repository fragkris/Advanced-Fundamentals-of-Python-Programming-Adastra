"""
The code draws cards from the deck and prints them with their total value.
I tried not to change the given code in the example.
"""

import random
from enum import Enum
from typing import Callable, Iterable, cast


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class BlackJackCard:

    def __init__(self, rank: str, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class AceCard(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)


#       ^ Introduce Ace card and its hard and soft values

class FaceCard(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10) \
            #       ^ Introduce Face card and its hard and soft values


class NumberCard(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


#       ^ Introduce Number card and its hard and soft values

def card_return(rank: int, suit: Suit) -> BlackJackCard:
    if rank == 1:
        return AceCard(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit)


#       ^ Returns a card


class Deck(list):
    def __init__(
            self, factory: Callable[[int, Suit], BlackJackCard] = card_return) -> None:
        super().__init__()
        for i in range(random.randint(1, 6)):
            self.extend(factory(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit))
        random.shuffle(self)


class Hand:
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard) -> None:
        self.dealer_card: BlackJackCard = dealer_card
        self._cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self._cards))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}, "
            f"{', '.join(map(repr, self._cards))})"
        )


class Hand_Lazy(Hand):
    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self._cards)
        hard_total = sum(c.hard for c in self._cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft
        return hard_total

    @property
    def card(self) -> list[BlackJackCard]:
        return self._cards

    @card.setter
    def card(self, aCard: BlackJackCard) -> None:
        self._cards.append(aCard)

    @card.deleter
    def card(self) -> None:
        self._cards.pop(-1)


d = Deck()
h = Hand_Lazy(d.pop(), d.pop(), d.pop())
print(h.total)
print(h)
