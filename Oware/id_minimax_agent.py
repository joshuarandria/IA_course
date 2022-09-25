from iterative_deepening import IterativeDeepening
from minimax_agent import MinimaxAgent


class IDMinimaxAgent(IterativeDeepening):
    def __init__(self):
        super().__init__(AgentClass=MinimaxAgent)