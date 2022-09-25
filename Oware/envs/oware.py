from envs.state import State, IllegalMove
from typing import List, Optional
from copy import deepcopy


class Oware(State):
    "A data structure to represent a state of Oware"

    # Constants
    MAX_TURNS = 240   # The maximum number of turns in each game
    INITIAL_STONES_PER_PIT = 4
    PITS_PER_PLAYER = 6
    PITS_COUNT = 2 * PITS_PER_PLAYER

    def __init__(self, player1: str, player2: str):
        super().__init__()
        self.__board = [self.INITIAL_STONES_PER_PIT for _ in range (self.PITS_COUNT)]
        self.__player = 0
        self.__players = (player1, player2)
        self.__collected = [0, 0]
        self.__actions = None
        self.__turn = 0

    @staticmethod
    def get_environment_name() -> str:
        return "Oware"

    def get_board(self) -> List[int]:
        """
        Return the number of stone in each pit

        Returns a list of integer describing how many store exists in each pit.
        NOTE: The return value is from the player perspective (i.e., the first
              half elements are for the current player and the second half
              elements are for the opponent).
        """
        if self.__player == 0:
            return self.__board[:]
        return self.__board[self.PITS_PER_PLAYER:] + self.__board[:self.PITS_PER_PLAYER]

    def get_collected_stone(self) -> List[int]:
        "Return collected stones of the current player and its opponent, respectively"

        return [self.__collected[self.__player], self.__collected[1 - self.__player]]

    def get_turn_number(self) -> int:
        return self.__turn

    def actions(self) -> List['Oware.__Action']:
        "Return all possible actions in the current state"

        if self.__actions is None:
            self.__actions = []
            for source in range(self.PITS_PER_PLAYER):
                try:
                    successor = self.__successor(source)
                    self.__actions.append(self.__Action(source, successor))
                except IllegalMove:
                    pass

        return self.__actions

    def successor(self, action: 'Oware.__Action') -> 'Oware':
        "Return the next state by applying the given action on the current state"

        if self.__actions is None:
            self.actions()
        if action not in self.__actions:
            raise IllegalMove("Illegal Move!")
        return action.successor()

    def is_winner(self) -> Optional[int]:
        """
        Determines if there is a winner in the current state or not

        This function can be used to determine if the game has ended or not, and
        if it is over, who is the winner.

        The return value is:
            `None`  => if the game is not over yet,
            `1`     => if the current player is the winner,
            `0`     => if the game ended in a draw, or,
            `-1`    => if the opponent won the game.
        """
        if self.__turn == self.MAX_TURNS:
            if self.__collected[self.__player] > self.__collected[1 - self.__player]:
                return 1
            if self.__collected[1 - self.__player] > self.__collected[self.__player]:
                return -1
            return 0

        if not self.actions():
            for pit in range(self.PITS_COUNT):
                self.__collected[self.__player] += self.__board[pit]
                self.__board[pit] = 0
            
        (players, collected) = ([0, 1], self.__collected) if self.__collected[0] >= self.__collected[1] else\
                               ([1, 0], [self.__collected[1], self.__collected[0]])
        STONES_COUNT = self.PITS_COUNT * self.INITIAL_STONES_PER_PIT
        if collected[0] > STONES_COUNT / 2:
            return int(collected[0] == self.__collected[self.__player]) * 2 - 1
        if collected[0] + collected[1] == STONES_COUNT:
            return 0
        return None

    def current_player(self) -> int:
        "Return the player index whose turn it is"
        return self.__player

    def get_players_names(self) -> List[str]:
        "Return the name of players"
        return list(self.__players)

    class __Action:
        def __init__(self, source, next_state: 'Oware'):
            self.source = source
            self.__next_state = next_state

        def successor (self) -> 'Oware':
            return self.__next_state

        def __str__(self):
            return f"{self.source}"

        def __eq__(self, __o: 'Oware.__Action') -> bool:
            return isinstance(__o, type(self)) and\
                   self.source == __o.source and\
                   self.__next_state == __o.__next_state

    def __get_next_state(self) -> 'Oware':
        next_state = deepcopy(self)
        next_state.__player = 1 - next_state.__player  # Switching the player
        next_state.__actions = None
        next_state.__turn += 1
        return next_state

    def __successor(self, source: int) -> 'Oware':
        if (not isinstance(source, int)) or source < 0 or source >= self.PITS_PER_PLAYER:
            raise IllegalMove(f"Action should be an integer in the range of [0, {self.PITS_PER_PLAYER})")
        source = source if self.__player == 0 else source + self.PITS_PER_PLAYER
        if self.__board[source] == 0:
            raise IllegalMove("The source pit must have at least one stone!")
        next_state = self.__get_next_state()
        destination = source
        while next_state.__board[source] > 0:
            destination = (destination + 1) % self.PITS_COUNT
            # if `source == destination` increasing and decreasing one to `source` is like skipping it
            next_state.__board[source] -= 1
            next_state.__board[destination] += 1

        opponents_pits = range(self.PITS_PER_PLAYER) if self.__player else range(self.PITS_PER_PLAYER, self.PITS_COUNT)
        if not any([next_state.__board[pit] for pit in opponents_pits]):
            raise IllegalMove("Opponent cannot play anymore!")

        before_capturing = deepcopy(next_state)
        while destination in opponents_pits and next_state.__board[destination] in [2, 3]:
            next_state.__collected[self.__player] += next_state.__board[destination]
            next_state.__board[destination] = 0
            destination = (destination - 1) % self.PITS_COUNT

        if not any([next_state.__board[pit] for pit in opponents_pits]):
            # opponent cannot play after capturing, so captured stones are forfeited
            return before_capturing
        return next_state

    def __str__(self) -> str:
        CELLS_INDEX_TEMPLATE = " " + " ".join([f"{{indices[{i}]: ^2d}}" for i in range(self.PITS_PER_PLAYER)]) + " \n"
        TOP_BOARDER          = "╔" + "╦".join(["══"                     for _ in range(self.PITS_PER_PLAYER)]) + "╗\n"
        CELLS_TEMPLATE       = "║" + "║".join([f"{{cells[{i}]: <2d}}"    for i in range(self.PITS_PER_PLAYER)]) + "║\n"
        MIDDLE_BOARDER       = "╠" + "╬".join(["══"                     for _ in range(self.PITS_PER_PLAYER)]) + "╣\n"
        BOTTOM_BOARDER       = "╚" + "╩".join(["══"                     for _ in range(self.PITS_PER_PLAYER)]) + "╝\n"
        output  = "Collected stones:\n"
        output += f"\t{self.__players[0]}: {self.__collected[0]}\n\t{self.__players[1]}: {self.__collected[1]}\n"
        output += f"Current player: {self.__players[self.__player]}\n\n"

        output += CELLS_INDEX_TEMPLATE.format(indices = [(2 - self.__player) * self.PITS_PER_PLAYER - i - 1
                                                         for i in range(self.PITS_PER_PLAYER)])
        output += TOP_BOARDER
        output += CELLS_TEMPLATE.format(cells = [self.__board[i - 1]
                                                 for i in range(self.PITS_COUNT, self.PITS_PER_PLAYER, -1)])
        output += MIDDLE_BOARDER
        output += CELLS_TEMPLATE.format(cells = [self.__board[i] for i in range(self.PITS_PER_PLAYER)])
        output += BOTTOM_BOARDER
        output += CELLS_INDEX_TEMPLATE.format(indices = [self.__player * self.PITS_PER_PLAYER + i
                                                         for i in range(self.PITS_PER_PLAYER)])
        return output

    def __hash__(self) -> int:
        return hash((tuple(self.__board), tuple(self.__collected), self.__player))

    def __eq__(self, __o: 'Oware') -> bool:
        return self.__board == __o.__board and\
               self.__player == __o.__player and\
               self.__players == __o.__players and\
               self.__collected == __o.__collected and\
               self.__turn == __o.__turn
