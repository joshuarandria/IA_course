from time import sleep
import tkinter as tk
import multiprocessing as mp
from envs.oware import Oware


class Visualizer:
    def __init__(self, initial_state: Oware):
        other_end, self.__connection = mp.Pipe()
        self.__process = mp.Process(target=self.start, args=(initial_state, other_end))
        self.__process.start()
    
    def start(self, initial_state, connection):
        from envs.oware_visualize import OwareVisualize

        try:
            visualizer = OwareVisualize(initial_state=initial_state)
            commands = {"activate_actions": visualizer.activate_actions,
                        "deactivate_actions": visualizer.deactivate_actions,
                        "apply_action": visualizer.apply_action,
                        "get_chosen_pit": visualizer.get_chosen_pit,
                        "game_over": visualizer.game_over}
            need_result = ["get_chosen_pit"]
            while not OwareVisualize.IS_CLOSED:
                if not connection.poll():
                    visualizer.refresh(0.01)
                    continue
                command, args, kw = connection.recv()
                result = commands[command](*args, **kw)
                if command in need_result:
                    connection.send(result)

            connection.close()
        except tk.TclError:
            pass
        except EOFError:
            pass

    def activate_actions(self, actions):
        offset = 0 if actions[0].successor().current_player() else Oware.PITS_PER_PLAYER
        pits = [offset + action.source for action in actions]
        args = (pits,)
        self.__connection.send(("activate_actions", args, {}))

    def deactivate_actions(self, *args, **kw):
        self.__connection.send(("deactivate_actions", args, kw))

    def apply_action(self, action):
        successor = action.successor()
        current_player = 1 - successor.current_player()
        source = action.source + (Oware.PITS_PER_PLAYER if current_player else 0)
        next_board = successor.get_board()
        if current_player == 0:
            next_board = next_board[Oware.PITS_PER_PLAYER:] + next_board[:Oware.PITS_PER_PLAYER]
        args = (current_player, source, next_board)
        self.__connection.send(("apply_action", args, {}))

    def get_chosen_pit(self, *args, **kw):
        self.__connection.send(("get_chosen_pit", args, kw))
        return self.__connection.recv()

    def game_over(self, *args, **kw):
        self.__connection.send(("game_over", args, kw))
        self.__process.join()