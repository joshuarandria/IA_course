from random import shuffle
from agent_interface import AgentInterface
from envs.oware import Oware
from random_agent import RandomAgent
from game import Game


class MCSAgent(AgentInterface):
    """
    Monte Carlo Search: Evaluate each action by taking it, followed by
    random plays. Action with most wins is chosen.
    """
    def __init__(self):
        self.__simulator = Game(RandomAgent(), RandomAgent())

    def info(self):
        return {"agent name": "MCS"}

    def decide(self, state: Oware, actions):
        shuffle(actions)
        win_counter = [0] * len(actions)
        counter = 0
        while True:
            counter += 1
            for i, action in enumerate(actions):
                state2 = state.successor(action)
                result = self.__simulator.play(output=False, starting_state=state2)
                win_counter[i] += 1 if result == [state.current_player()] else 0
            yield actions[win_counter.index(max(win_counter))]
