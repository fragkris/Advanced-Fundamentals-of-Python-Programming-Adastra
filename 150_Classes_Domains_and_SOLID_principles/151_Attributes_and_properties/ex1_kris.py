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


class Ace_Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)


class Face_Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)\


class Number_Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


def card_return(rank: int, suit: Suit) -> BlackJackCard:
    if rank == 1:
        return Ace_Card(rank, suit)
    elif 2 <= rank < 11:
        return Number_Card(rank, suit)
    elif 11 <= rank < 14:
        return Face_Card(rank, suit)



class Deck(list):
    def __init__(
            self, decks: int = 6, factory: Callable[[int, Suit], BlackJackCard] = card_return) -> None:
        super().__init__()
        for i in range(decks):
            self.extend(factory(r + 1, s) for r in range(13) for s in cast(Iterable[Suit], Suit))
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


class Hand:
    def __init__(
            self,
            dealer_card: BlackJackCard,
            *cards: BlackJackCard ) -> None:
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