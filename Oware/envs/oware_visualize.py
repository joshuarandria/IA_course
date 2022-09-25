from random import choices, shuffle
from typing import List
import tkinter as tk
from tkinter.font import Font as tkFont
from PIL import Image, ImageTk
from time import sleep, time

from envs.oware import Oware


class OwareVisualize:
    ROOT = tk.Tk()
    ROOT.title("Oware (CS-E4800 Tournament)")
    ROOT.iconphoto(True, tk.PhotoImage(file="images/AI.png"))
    IS_CLOSED = False

    # @staticmethod
    # def on_quit():
    #     OwareVisualize.IS_CLOSED = True
    #     OwareVisualize.ROOT.destroy()
    # ROOT.protocol("WM_DELETE_WINDOW", on_quit)

    STONES = [f"images/stone{i}.png" for i in range(10)]
    stones = []
    BOARD = "images/board.png"
    BOARD_SIZE = (2560, 1440)
    GAME_OVER = "images/game_over.png"
    PIT_LENGTH = 350
    PITS_X_OFFSET = 230
    PITS_Y_OFFSET = 720
    STORAGE_HEIGHT = 320
    selected_pit = None

    class Pit:
        MARGIN = 112
        SAMPLE_POINTS = 50
        ACTIVE_LIGHTS = ["images/active_bottom.png", "images/active_up.png"]
        SELECT_LIGHTS = ["images/select_bottom.png", "images/select_up.png"]

        def __init__(self, canvas: 'ResizableCanvas', x_offset, y_offset, width, height, stones, pit_id):
            x0, y0 = (x_offset + self.MARGIN, y_offset + self.MARGIN)
            x1, y1 = (x_offset + width - self.MARGIN, y_offset + height - self.MARGIN)
            self.bounding_box = (x0, y0, x1, y1)
            self.stones = []
            for stone in range(stones):
                if not OwareVisualize.stones:
                    OwareVisualize.stones = OwareVisualize.STONES[:]
                    shuffle(OwareVisualize.stones)
                position = self.__find_position()
                stone = canvas.create_image(position[0], position[1], file=OwareVisualize.stones.pop())
                self.stones.append((stone, position))

            self.activation = canvas.create_image(x_offset,
                                                  y_offset,
                                                  file=self.ACTIVE_LIGHTS[pit_id // Oware.PITS_PER_PLAYER],
                                                  anchor=tk.NW,
                                                  state='hidden')
            self.selection = canvas.create_image(x_offset,
                                                 y_offset,
                                                 file=self.SELECT_LIGHTS[pit_id // Oware.PITS_PER_PLAYER],
                                                 anchor=tk.NW,
                                                 state='hidden')

            def choose_this_pit(_):
                OwareVisualize.selected_pit = pit_id
            canvas.tag_bind(self.activation, "<Button-1>", choose_this_pit)

        def get_stones(self):
            stones = self.stones
            self.stones = []
            return stones

        def put_stone(self, stone):
            position = self.__find_position()
            self.stones.append((stone, position))
            return position

        def activate(self, canvas):
            canvas.tag_raise(self.activation)
            canvas.itemconfigure(self.activation, state='normal')

        def deactivate(self, canvas):
            canvas.itemconfigure(self.activation, state='hidden')

        def select(self, canvas):
            canvas.itemconfigure(self.selection, state='normal')

        def deselect(self, canvas):
            canvas.itemconfigure(self.selection, state='hidden')

        def __find_position(self):
            max_min_distance = -1
            best_x = best_y = None
            x0, y0, x1, y1 = self.bounding_box
            for x, y in zip(choices(range(x0, x1), k=self.SAMPLE_POINTS), choices(range(y0, y1), k=self.SAMPLE_POINTS)):
                min_distance = 2 * (OwareVisualize.PIT_LENGTH ** 2)
                for _, (xx, yy) in self.stones:
                    distance = (x - xx) ** 2 + (y - yy) ** 2
                    min_distance = min(min_distance, distance)
                if min_distance > max_min_distance:
                    max_min_distance = min_distance
                    best_x, best_y = x, y
            return best_x, best_y


    def __init__(self, initial_state: Oware):
        #refresh Canvas
        for old_items in self.ROOT.winfo_children():
            old_items.destroy()
        self.canvas = ResizableCanvas(self.ROOT, width=self.BOARD_SIZE[0], height=self.BOARD_SIZE[1])
        width = self.ROOT.winfo_screenwidth()
        width = min(width // 1.5, int(self.BOARD_SIZE[0] * 0.75))
        self.canvas.resize(width=width, height=None)
        self.canvas.pack(fill="both", expand=True)
        self.ROOT.eval('tk::PlaceWindow . center')
        self.canvas.create_image(0, 0, anchor=tk.NW, file=self.BOARD)
        xOffset = self.PITS_X_OFFSET
        yOffset = self.PITS_Y_OFFSET
        self.pits = []
        pit_length = self.PIT_LENGTH
        for i, stones in enumerate(self.get_board(initial_state)):
            self.pits.append(self.Pit(self.canvas, xOffset, yOffset, self.PIT_LENGTH, self.PIT_LENGTH, stones, i))
            if i == Oware.PITS_PER_PLAYER - 1:
                yOffset -= pit_length
                pit_length = -pit_length
            else:
                xOffset += pit_length
        self.storages = [self.Pit(self.canvas,
                                  self.PITS_X_OFFSET, 
                                  self.PITS_Y_OFFSET + self.PIT_LENGTH,
                                  (Oware.PITS_PER_PLAYER - 2) * self.PIT_LENGTH,
                                  self.STORAGE_HEIGHT,
                                  0,
                                  0), #None),
                         self.Pit(self.canvas,
                                  self.PITS_X_OFFSET,
                                  self.PITS_Y_OFFSET - self.PIT_LENGTH - self.STORAGE_HEIGHT,
                                  (Oware.PITS_PER_PLAYER - 2) * self.PIT_LENGTH,
                                  self.STORAGE_HEIGHT,
                                  0,
                                  0)] #None)]

        style = {"size": 48, "fill": "#6e2600"}
        self.__score_texts = [self.canvas.create_text(2, self.BOARD_SIZE[1], anchor=tk.SW, **style),
                            self.canvas.create_text(2, 0, anchor=tk.NW, **style)]
        self.__scores = [-1, -1]
        self.players_names = initial_state.get_players_names()
        self.__last_refresh_time = 0
        self.__refresh_scores()

    @staticmethod
    def get_board(state: Oware) -> List[int]:
        board = state.get_board()
        if state.current_player() == 0:
            return board
        return board[Oware.PITS_PER_PLAYER:] + board[:Oware.PITS_PER_PLAYER]

    def activate_actions(self, pits):
        for pit in pits:
            self.pits[pit].activate(self.canvas)
        self.refresh()

    def deactivate_actions(self):
        for pit in self.pits:
            pit.deactivate(self.canvas)
        self.refresh()

    def get_chosen_pit(self):
        OwareVisualize.selected_pit = None
        while OwareVisualize.selected_pit is None:
            self.refresh(0.01)
        result = OwareVisualize.selected_pit
        OwareVisualize.selected_pit = None
        return result

    def apply_action (self, current_player, source, next_board):
        destination = self.__sowing(source)
        self.__capturing(destination, current_player, next_board)
        self.__refresh_scores()

    def game_over(self, winners: List[int]):
        x, y = (self.BOARD_SIZE[0] / 2, self.BOARD_SIZE[1] / 2)
        self.canvas.create_image(x, y, file=self.GAME_OVER, anchor=tk.CENTER)
        style = {"size": 64, "fill": "#6e2600"}
        if len(winners) != 1:
            winner = "The game ended in a draw!"
        else:
            winner = f"Player {winners[0]}, {self.players_names[winners[0]]}, WON!"
        self.canvas.create_text(x, y, text="Game is over", anchor=tk.S, **style),
        self.canvas.create_text(x, y, text=winner, anchor=tk.N, **style),
        self.refresh()
        self.refresh(7)
        self.IS_CLOSED = True

    def __sowing (self, source: int):
        picked_stones = [stone for (stone, _) in self.pits[source].get_stones()]
        for stone in picked_stones:
            self.canvas.tag_raise(stone)
        if source < Oware.PITS_PER_PLAYER:
            self.__move(picked_stones, 0, 384)
        else:
            self.__move(picked_stones, 0, -384)
        destination = source
        while picked_stones:
            destination = (destination + 1) % Oware.PITS_COUNT
            if destination == 0:
                x = 0
                y = self.PIT_LENGTH + 768
            elif destination < Oware.PITS_PER_PLAYER:
                x = self.PIT_LENGTH
                y = 0
            elif destination == Oware.PITS_PER_PLAYER:
                x = 0
                y = -self.PIT_LENGTH - 768
            else:
                x = -self.PIT_LENGTH
                y = 0
            self.__move(picked_stones, x, y)
            if destination == source:
                continue
            stone = picked_stones.pop()
            (x_position, y_position) = self.pits[destination].put_stone(stone)
            self.__move_to(stone, x_position, y_position)
        return destination

    def __capturing(self, destination, current_player, next_board):
        opponent_pits = range(Oware.PITS_PER_PLAYER, Oware.PITS_COUNT) if current_player == 0\
                                                                       else range(Oware.PITS_PER_PLAYER)
        while destination in opponent_pits and next_board[destination] == 0:
            for stone, _ in self.pits[destination].get_stones():
                (x_position, y_position) = self.storages[current_player].put_stone(stone)
                self.__move_to(stone, x_position, y_position)
            destination = (destination - 1) % Oware.PITS_COUNT

    def __move_to(self, object, x_position, y_position):
        x_current, y_current = self.canvas.get_image_coordinate(object)
        x_move = x_position - x_current
        y_move = y_position - y_current
        self.__move([object], x_move, y_move)

    def __move(self, objects, x_move, y_move):
        length = abs((x_move * 100) // self.BOARD_SIZE[0]) + abs((y_move * 100) // (3 * self.BOARD_SIZE[1]))
        STEPS_COUNT = min(int(length * 0.75), 15)
        x_step = x_move / STEPS_COUNT
        y_step = y_move / STEPS_COUNT
        x_remains = 0
        y_remains = 0
        for _ in range(STEPS_COUNT):
            x = x_step + x_remains
            y = y_step + y_remains
            x_remains = x - int(x)
            y_remains = y - int(y)
            for object in objects:
                self.canvas.image_move(object, int(x), int(y))
            self.refresh(0.02)
        self.refresh()

    def __refresh_scores(self):
        new_scores = [len(self.storages[i].stones) for i in [0, 1]]
        if new_scores == self.__scores:
            return
        for i in [0, 1]:
            self.canvas.itemconfigure(self.__score_texts[i],
                                      text=f"Player {i}: {self.players_names[i]} ({new_scores[i]})")
        self.__scores = new_scores
        self.refresh()

    def refresh(self, after=0):
        sleeping_time = after - (time() - self.__last_refresh_time)
        sleep(sleeping_time if sleeping_time > 0 else 0)
        if self.IS_CLOSED:
            exit()
        self.ROOT.update_idletasks()
        self.ROOT.update()
        self.__last_refresh_time = time()


class ResizableCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent,**kwargs)
        self.config(highlightthickness=0)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.x_scale = 1
        self.y_scale = 1
        self.images = {}
        self.texts = {}

    def create_image(self, x, y, *args, **kw):
        new_x, new_y = self.__new_position(x, y)
        image = Image.open(kw.pop('file'))
        new_image = image.copy().resize(self.__new_position(*image.size))
        tk_image = ImageTk.PhotoImage(new_image)
        image_id = super().create_image(new_x, new_y, *args, image=tk_image, **kw)
        self.images[image_id] = [x, y, image, tk_image]
        return image_id

    def image_move(self, image_id, x, y):
        self.images[image_id][0] += x
        self.images[image_id][1] += y
        self.coords(image_id, *self.__new_position(*self.images[image_id][:2]))

    def image_move_to(self, image_id, x, y):
        self.images[image_id][0] = x
        self.images[image_id][1] = y
        self.coords(image_id, *self.__new_position(x, y))

    def get_image_coordinate(self, image_id):
        return self.images[image_id][:2]

    def get_style(self, size: int):
        return {"font": tkFont(family="Cooper Black", size=int(size * self.y_scale), weight='bold')}

    def create_text(self, x, y, *args, **kw):
        size = kw.pop('size')
        kw.update(self.get_style(size))
        text_id = super().create_text(*self.__new_position(x, y), *args, **kw)
        self.texts[text_id] = [x, y, size]
        return text_id

    def on_resize(self, event):
        self.resize(event.width, event.height)

    def resize(self, width, height):
        # determine the ratio of old width/height to new width/height
        if width == None:
            width = self.width * (height / self.height)
        if height == None:
            height = self.height * (width / self.width)
        self.x_scale = width / self.width
        self.y_scale = height / self.height
        # resize the canvas 
        self.config(width=width, height=height)
        # resize all images
        for image_id, (x, y, image, _) in self.images.items():
            new_image = image.copy()
            new_size = (int(new_image.size[0] * self.x_scale), int(new_image.size[1] * self.y_scale))
            new_image = new_image.resize(new_size, Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(new_image)
            self.images[image_id][3] = tk_image
            self.itemconfigure(image_id, image=tk_image)
            self.coords(image_id, *self.__new_position(x, y))

        for text_id, (x, y, size) in self.texts.items():
            self.coords(text_id, *self.__new_position(x, y))
            self.itemconfigure(text_id, self.get_style(size))

    def __new_position(self, x, y):
        return (int(self.x_scale * x), int(self.y_scale * y))


if __name__ == "__main__":
    state = Oware("T", "F")
    visualizer = OwareVisualize(state)
    actions = state.actions()
    sleep(1)
    visualizer.apply_action(actions[0])
    visualizer.ROOT.mainloop()