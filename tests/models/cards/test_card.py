from onestep.models.cards.card import SlashCard

from onestep.models.characters.character import Character
from onestep.models.characters.attributes import EnergyOverspendException
import pytest  # type: ignore


def test_attributes():
    c1 = Character.new_basic(20, 1)
    c2 = Character.new_basic(20, 20)

    card = SlashCard(10)
    card.apply(c1, c2)
    assert c1.energy == 0, "Character should have no energy left"
    assert c2.health == 10, "Character should only have 10 health now"

    with pytest.raises(EnergyOverspendException) as i_info:
        card.apply(c1, c2)

    assert c2.health == 10, "Character should still have 10 health now"


