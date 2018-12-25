from random import shuffle
from typing import List

from onestep.models.cards.card import Card, SlashCard


class NotEnoughCardsInStackException(Exception):
    pass


class BaseCardCollection:
    def __init__(self, cards: List[Card]):
        self._cards = cards

    def __len__(self):
        return len(self._cards)


class Deck(BaseCardCollection):
    def __init__(self, name: str, cards: List[Card]):
        super().__init__(cards)
        self.name = name

    @classmethod
    def new_basic(cls, card_amount: int) -> "Deck":
        cards: List[Card] = [SlashCard(i * 2 + 1) for i in range(card_amount)]
        deck = Deck("Basic Deck", cards)
        return deck

    def add_card(self, card: Card):
        self._cards.append(card)
        sorted(self._cards)

    @property
    def cards(self):
        return self._cards


class Hand(BaseCardCollection):
    def __init__(self):
        super().__init__([])

    def add(self, cards: List[Card]):
        self._cards.extend(cards)

    def draw_at_index(self, index: int) -> Card:
        return self._cards.pop(index)

class DiscardPile(BaseCardCollection):
    def __init__(self):
        super().__init__([])

    def add(self, card: Card):
        self._cards.append(card)


class Stack(BaseCardCollection):

    def __init__(self, cards: List[Card]):
        super().__init__(cards)

    def draw(self, amount: int) -> List[Card]:
        if amount > len(self):
            raise NotEnoughCardsInStackException()

        shuffle(self._cards)
        head, tail = self._cards[:amount], self._cards[amount:]
        self._cards = tail
        return head

    @classmethod
    def from_deck(cls, deck: Deck) -> "Stack":
        return cls(deck.cards[:])
