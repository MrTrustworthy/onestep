from typing import Dict, List, Optional

from names import get_full_name  # type: ignore

from onestep.models.cards.cardcollections import Stack, Deck, Hand, DiscardPile
from onestep.models.characters.attributes import AttributeName, Attribute


class Character:

    def __init__(self, name: str, base_attributes: Dict[AttributeName, Attribute], deck: Deck):
        self.name = name
        self.health = base_attributes[AttributeName.HEALTH]
        self.energy = base_attributes[AttributeName.ENERGY]
        self.draw_amount = base_attributes[AttributeName.DRAW_AMOUNT]
        self.initiative = base_attributes[AttributeName.INITIATIVE]

        self.deck = deck
        self.active_stack: Optional[Stack] = None  # Set and cleared by the battle controller at start/end of battles
        self.active_hand: Optional[Hand] = None  # Set and cleared by the battle controller at start/end of battles
        self.active_pile: Optional[DiscardPile] = None  # Set and cleared by the battle controller at start/end of battles


    @property
    def alive(self) -> bool:
        return self.health > 0  # type: ignore

    @classmethod
    def new_basic(
            cls,
            health: int,
            energy: int,
            deck_size: int = 5,
            draw_amount: int = 3,
            initiative: int = 5
    ) -> "Character":
        base_attributes = {
            AttributeName.HEALTH: Attribute(AttributeName.HEALTH, health),
            AttributeName.ENERGY: Attribute(AttributeName.ENERGY, energy),
            AttributeName.DRAW_AMOUNT: Attribute(AttributeName.DRAW_AMOUNT, draw_amount),
            AttributeName.INITIATIVE: Attribute(AttributeName.INITIATIVE, initiative)
        }
        name = get_full_name()

        deck = Deck.new_basic(deck_size)

        return cls(name, base_attributes, deck)


class Group:
    def __init__(self, characters: List[Character]):
        self._characters = characters

    @property
    def alive(self):
        return any(c.alive for c in self._characters)

    def __iter__(self):
        yield from self._characters