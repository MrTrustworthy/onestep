from itertools import chain
from typing import Optional

from onestep.controllers.battleinputcontroller import BattleInputController, BattleInputCardUseCommand, \
    BattleInputEndTurnCommand
from onestep.models.cards.cardcollections import Hand, Stack, DiscardPile
from onestep.models.characters.character import Character, Group


class BattleController:

    def __init__(self, group_a: Group, group_b: Group, input_controller: BattleInputController):
        self.group_a = group_a
        self.group_b = group_b
        self.all_characters = list(chain(group_a, group_b))
        self.input_controller = input_controller

    def run_battle_loop(self) -> Optional[Group]:
        for character in self.all_characters:
            BattleController.prepare_character(character)

        while self.group_a.alive and self.group_b.alive:
            self.run_turn()

        if self.group_a.alive:
            return self.group_a
        elif self.group_b.alive:
            return self.group_b
        else:
            return None

    def run_turn(self):
        order = sorted(self.all_characters, key=lambda c: c.initiative.current)

        for character in order:
            self._run_character_turn(character)

    def _run_character_turn(self, character):
        while True:
            input_command = self.input_controller.get_input_for(character)
            if isinstance(input_command, BattleInputEndTurnCommand):
                break
            elif isinstance(input_command, BattleInputCardUseCommand):
                card = character.active_hand.draw_at_index(input_command.card_hand_idx)
                target = self.all_characters[input_command.target_index]
                card.apply(character, target)
            else:
                raise AttributeError("No way to handle this command")

    @staticmethod
    def prepare_character(char: Character):
        char.active_stack = Stack.from_deck(char.deck)
        char.active_hand = Hand()
        char.active_pile = DiscardPile()
        drawn = char.active_stack.draw(char.draw_amount.current)
        char.active_hand.add(drawn)
