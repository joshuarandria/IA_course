from agent_interface import AgentInterface
from typing import Type


class IterativeDeepening(AgentInterface):
    def __init__(self, AgentClass: Type[AgentInterface], *args, **kwargs):
        MAX_DEPTH = 1000
        self.__agents = list()
        for depth in range(1, MAX_DEPTH):
            self.__agents.append(AgentClass(*args, depth=depth, **kwargs))

    def info(self):
        return {'agent name': f'ID-{self.__agents[0].info()["agent name"]}'}

    def decide(self, *args, **kwargs):
        for agent in self.__agents:
            for decision in agent.decide(*args, **kwargs):
                yield decision
