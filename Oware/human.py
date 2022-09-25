from envs.oware import Oware
from agent_interface import AgentInterface


class Human(AgentInterface):
    """
    The Human controlling agent who plays the Oware game
    """
    def __init__(self):
        super().__init__()
        self.__board = None

    def set_board(self, board):
        self.__board = board

    @staticmethod
    def info():
        return {"agent name": "Human"}

    def decide(self, state: Oware, actions: list):
        best_move = self.__board.get_chosen_pit()
        if best_move >= Oware.PITS_PER_PLAYER:
            best_move -= Oware.PITS_PER_PLAYER
        for action in actions:
            if action.source == best_move:
                yield action
