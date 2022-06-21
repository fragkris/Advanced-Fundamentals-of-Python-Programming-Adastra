import random
from enum import Enum
from typing import Callable, Iterable, cast


class BlackJackCard:

    def __init__(self, rank: str, suit: "Suit", hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit!r}, hard={self.hard}, soft={self.soft}"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Ace21Card(BlackJackCard):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank=1, suit={self.suit!r})"


class Face21Card(BlackJackCard):
    __slots__ = ("rank", "suit", "hard", "soft")

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)

    def __repr__(self) -> str:
        rank_num = {"J": 11, "Q": 12, "K": 13}[self.rank]
        return f"{self.__class__.__name__}(rank={rank_num}, suit={self.suit!r})"


class Number21Card(BlackJackCard):
    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit!r})"


def card21(rank: int, suit: Suit) -> BlackJackCard:
    if rank == 1:
        return Ace21Card(rank, suit)
    elif 2 <= rank < 11:
        return Number21Card(rank, suit)
    elif 11 <= rank < 14:
        return Face21Card(rank, suit)
    else:
        raise TypeError


class Deck(list):
    def __init__(
            self, decks: int = 6, factory: Callable[[int, Suit], BlackJackCard] = card21) -> None:
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
        return ", ".join(map(str, self.card))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.dealer_card!r}, "
            f"{', '.join(map(repr, self.card))})"
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