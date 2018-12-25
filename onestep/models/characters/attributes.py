from enum import Enum
from functools import total_ordering
from typing import List, Any


class EnergyOverspendException(Exception):
    pass


class AttributeName(Enum):
    HEALTH = "Health"
    ENERGY = "Energy"
    DRAW_AMOUNT = "Draw Amount"
    INITIATIVE = "Initiative"


class AttributeModifier:

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def apply(self, attribute_value: int) -> int:
        return attribute_value + self.value

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.value == other.value


class AttributeModifiers:
    def __init__(self):
        self._modifiers: List[AttributeModifier] = []

    def add(self, modifier: AttributeModifier):
        self._modifiers.append(modifier)

    def apply_all(self, value):
        for modifier in self._modifiers:
            value = modifier.apply(value)
        return value


@total_ordering
class Attribute:

    def __init__(self, name: AttributeName, max_val: int):
        self.name = name
        self._max = max_val
        self._modifiers = AttributeModifiers()

    @property
    def current(self) -> int:
        return self._modifiers.apply_all(self._max)

    def add_modifier(self, modifier: AttributeModifier):
        self._modifiers.add(modifier)

    def clear_modifiers(self):
        self._modifiers = []

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Attribute):
            return self.current == other.current
        elif isinstance(other, int):
            return self.current == other
        else:
            raise AttributeError("Can't compare a Attribute with something other than Attributes or Integers")

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Attribute):
            return self.current < other.current
        elif isinstance(other, int):
            return self.current < other
        else:
            raise AttributeError("Can't compare a Attribute with something other than Attributes or Integers")
