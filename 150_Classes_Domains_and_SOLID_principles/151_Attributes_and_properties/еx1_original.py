from enum import Enum


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


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