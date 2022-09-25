from typing import List, Optional


class State:

    def __init__(self):
        pass

    @staticmethod
    def get_environment_name () -> str:
        raise NotImplementedError

    def actions(self):
        raise NotImplementedError

    def successor(self, action) -> 'State':
        raise NotImplementedError

    def is_winner(self) -> Optional[List[int]]:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError


class IllegalMove(ValueError):
    pass