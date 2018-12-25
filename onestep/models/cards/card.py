from enum import Enum
from random import shuffle
from typing import TYPE_CHECKING, List, Any, Sequence
from functools import total_ordering

from onestep.models.characters.attributes import AttributeModifier, EnergyOverspendException

if TYPE_CHECKING:
    from onestep.models.characters.character import Character


class CardRarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    MAGIC = 3
    RARE = 4
    EPIC = 5


class CardType(Enum):
    MAGIC = "Magic"
    PHYSICAL = "Physical"
    INNER = "Inner"


@total_ordering
class Card:

    def __init__(
            self,
            name: str,
            energy_cost: int,
            *,
            card_type: CardType = CardType.PHYSICAL,
            rarity: CardRarity = CardRarity.COMMON
    ):
        self.name = name
        self.energy_cost = energy_cost
        self.rarity = rarity
        self.card_type = card_type

    def apply(self, source: "Character", target: "Character"):
        energy = AttributeModifier(f"Energy cost from using {self.name}", -self.energy_cost)
        source.energy.add_modifier(energy)
        if source.energy.current < 0:
            raise EnergyOverspendException(f"Spent too much energy, now left at {source.energy.current}")

    def __eq__(self, other: Any) -> bool:
        return self.name == other.name and self.energy_cost == other.energy_cost and self.rarity == other.rarity

    def __gt__(self, other: Any) -> bool:
        return self.rarity.value > other.rarity.value or self.name < other.name


class SlashCard(Card):
    def __init__(self, strength: int):
        super().__init__("Slash", 1)
        self.strength = strength

    def apply(self, source: "Character", target: "Character"):
        super().apply(source, target)
        target_dmg = AttributeModifier("Plain Damage", -self.strength)
        target.health.add_modifier(target_dmg)



