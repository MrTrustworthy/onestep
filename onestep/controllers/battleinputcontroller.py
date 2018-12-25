from onestep.models.characters.character import Character


class BattleInputCommand:
    pass


class BattleInputCardUseCommand(BattleInputCommand):
    def __init__(self, card_hand_idx: int, target_index: int):
        self.card_hand_idx = card_hand_idx
        self.target_index = target_index


class BattleInputEndTurnCommand(BattleInputCommand):
    pass


class BattleInputController:

    def get_input_for(self, char: Character) -> BattleInputCommand:
        raise NotImplementedError("Needs to be implemented in subclasses")
