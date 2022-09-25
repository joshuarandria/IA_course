from agent_interface import AgentInterface
from envs.state import State, IllegalMove
from time_limit import time_limit

import time
from typing import List
from copy import deepcopy
from random import choice


class Game:
    def __init__(self, player1: AgentInterface, player2: AgentInterface):
        self.__players = [player1, player2]

    def play(self, starting_state: State, output=False, visualizer=None, timeout_per_turn=[None, None]):
        winners = self.__play(starting_state, output, visualizer, timeout_per_turn)
        if output:
            print("Game is over!")
            if len(winners) == 0:
                print("The game ended in a draw!")
            else:
                print(f"Player {winners[0]}, {starting_state.get_players_names()[winners[0]]}, WON!")
        if visualizer:
            visualizer.game_over(winners)
        return winners

    def __play(self, state, output, visualizer, timeout_per_turn) -> List[int]:
        duration = None
        action = None
        while True:
            if output:
                if duration is not None:
                    print(f"Decision time: {duration:0.3f}")
                    print("Action:", action)
                    print("=======================================================")
                print(state)
            is_winner = state.is_winner()
            if is_winner is not None:
                if is_winner == 0:
                    return []
                if is_winner == 1:
                    return [state.current_player()]
                return [1 - state.current_player()]
            actions = state.actions()
            if visualizer:
                visualizer.activate_actions(actions)
            start_time = time.time()
            action = self.__get_action(self.__players[state.current_player()],
                                       state,
                                       actions,
                                       timeout_per_turn[state.current_player()])
            duration = time.time() - start_time
            try:
                state = state.successor(action)
            except IllegalMove:
                if action is None:
                    print ("Time out!")
                else:
                    print("Illegal move!")
                print("Choosing a random action!")
                action = choice(actions)
                state = state.successor(action)
            if visualizer is not None:
                visualizer.deactivate_actions()
                visualizer.apply_action(action)

    def __get_action(self, player, state, actions, timeout):
        action = None
        try:
            with time_limit(timeout):
                for decision in player.decide(deepcopy(state), deepcopy(actions)):
                    action = decision
        except TimeoutError:
            pass
        return action
