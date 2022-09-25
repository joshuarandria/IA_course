import random
from agent_interface import AgentInterface
from envs.oware import Oware


class MinimaxAgent(AgentInterface):
    """
    An agent who plays the Oware game using Minimax algorithm
    """

    def __init__(self, depth: int = 4):
        self.depth = depth

    def info(self):
        return {"agent name": "Minimax"}

    def heuristic(self, state: Oware):
        collected_stones = state.get_collected_stone()
        return collected_stones[0] - collected_stones[1] 

    def decide(self, state: Oware, actions: list):
        """
        Get the value of each action by passing its successor to min_value
        function.
        """
        random.shuffle(actions)
        best_action = actions[0]
        max_value = float('-inf')
        for action in actions:
            action_value = self.min_value(state.successor(action), self.depth - 1)
            if action_value > max_value:
                max_value = action_value
                best_action = action
        yield best_action

    def max_value(self, state: Oware, depth: int):
        """
        Get the value of each action by passing its successor to min_value
        function. Return the maximum value of successors.
        
        `max_value()` function sees the game from players's perspective, trying
        to maximize the value of next state.
        
        NOTE: when passing the successor to min_value, `depth` must be
        reduced by 1, as we go down the Minimax tree.
        
        NOTE: the player must check if it is the winner (or loser)
        of the game, in which case, a large value (or a negative value) must
        be assigned to the state. Additionally, if the game is not over yet,
        but we have `depth == 0`, then we should return the heuristic value
        of the current state.
        """

        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('inf')
        if depth == 0:
            return self.heuristic(state)

        # If it is not terminated
        actions = state.actions()
        value = float('-inf')
        for action in actions:
            value = max(value, self.min_value(state.successor(action), depth - 1))
        return value

    def min_value(self, state, depth):
        """
        Get the value of each action by passing its successor to max_value
        function. Return the minimum value of successors.
        
        `min_value()` function sees the game from opponent's perspective, trying
        to minimize the value of next state.
        
        NOTE: when passing the successor to max_value, `depth` must be
        reduced by 1, as we go down the Minimax tree.

        NOTE: the opponent must check if it is the winner (or loser)
        of the game, in which case, a negative value (or a large value) must
        be assigned to the state. Additionally, if the game is not over yet,
        but we have `depth == 0`, then we should return the heuristic value
        of the current state.
        """

        # Termination conditions
        is_winner = state.is_winner()
        if is_winner is not None:
            return is_winner * float('-inf')
        if depth == 0:
            return -self.heuristic(state)  # Because heuristic value is calculated for the current player, which is the
                                           # opponent, we should multiply it with -1

        # If it is not terminated
        actions = state.actions()
        value = float('inf')
        for action in actions:
            value = min(value, self.max_value(state.successor(action), depth - 1))
        return value