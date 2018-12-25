import pytest  # type: ignore

from onestep.controllers.battlecontroller import BattleController
from onestep.controllers.battleinputcontroller import BattleInputController, \
    BattleInputCardUseCommand, BattleInputEndTurnCommand
from onestep.models.cards.cardcollections import NotEnoughCardsInStackException
from onestep.models.characters.character import Group, Character


class ShimInputController(BattleInputController):

    def __init__(self):
        super().__init__()
        self.toggle = False

    def get_input_for(self, char: Character):
        if self.toggle:
            self.toggle = not self.toggle
            return BattleInputEndTurnCommand()
        else:
            self.toggle = not self.toggle
            return BattleInputCardUseCommand(0, 0)


def test_battle_prep():
    bc = BattleController(Group([]), Group([]), BattleInputController())

    c = Character.new_basic(20, 20)

    bc.prepare_character(c)

    assert len(c.active_hand) == c.draw_amount.current
    assert len(c.active_stack) == (len(c.deck) - c.draw_amount.current)

    with pytest.raises(NotEnoughCardsInStackException):
        c.active_stack.draw(3)


def test_battle_exec():
    c1 = Character.new_basic(20, 20)
    c2 = Character.new_basic(20, 20)
    g1 = Group([c1])
    g2 = Group([c2])

    bc = BattleController(g1, g2, ShimInputController())
    winner = bc.run_battle_loop()
    assert winner in (g1, g2)
    print("Winner is", winner)
