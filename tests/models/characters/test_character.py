from onestep.models.characters.character import Character
from onestep.models.characters.attributes import AttributeModifier


def test_attributes():
    c = Character.new_basic(20, 20)
    assert c.name, "Character Should have a non-falsy name"
    assert c.health > 0, "Character should have more than 0 health"
    assert c.alive, "Character should be alive"
    assert c.energy > 0, "Character should have some energy"

    damage = AttributeModifier("Plain Damage", -10)

    c.health.add_modifier(damage)
    assert c.health == 10, "Health should now be 10"

    c.health.add_modifier(damage)
    assert c.health == 0, "Health should now be 10"
    assert not c.alive, "Character should be dead"
