#!/usr/bin/python3

# NOTE: It is recommended to only add the missing code
# in places marked with comments ###
#
# NOTE 2: Do not change the name of the class or the methods, as
# the automated grader relies on the names.

from mimetypes import init
import time
import queue

# Creating a grid for the Pac-Man to wander around.
# The grid is given as a list of string, e.g.
# [".......",
#  ".XXX.X.",
#  ".XXX...",
#  ".XXX.X.",
#  ".....X.",
#  ".XXXXX.",
#  "......."]
# Here the important information is the size of the grid,
# in Y direction the number of string, and in the X direction
# the length of the strings, and whether there is X in
# a grid cell. Pac-Man can enter any cell that is not a wall
# cell marked with X.
# The bottom left cell is (0,0). Cells outside the explicitly
# stated grid are all wall cells.


class PacManGrid:
    def __init__(self, grid):
        self.grid = grid
        self.xmax = len(grid[0]) - 1
        self.ymax = len(grid) - 1

    # Test whether the cell (x,y) is wall.

    def occupied(self, x, y):
        if x < 0 or y < 0 or x > self.xmax or y > self.ymax:
            return True
        s = self.grid[self.ymax-y]
        return (s[x] == 'X')

# State space search problems are represented in terms of states.
# For each state there are a number of actions that are applicable in
# that state. Any of the applicable actions will produce a successor
# state for the state. To use a state space in search algorithms, we
# also need functions for producing a hash value for a state
# (the function hash) and for testing equality of two states.
#
# In this exercise we represent states as Python classes with the
# following components.
#
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns a list [(a1,s1),...,(aN,sN)] where each si
#               is the successor state when action ai is taken.
#               Here the name ai of an action is a string.

# The state of the Pac-Man (given a grid) consists of
# three components:
# x: the X coordinate 0..self.grid.xmax
# y: the Y coordinate 0..self.grid.ymax
# d: the direction "N", "S", "E", "W" Pac-Man is going
# Based on this information, the possible successor states
# of (x,y,d) are computed by 'successors'.


class PacManState:

    # Creating a state:

    def __init__(self, x, y, direction, grid):
        self.x = x
        self.y = y
        self.d = direction
        self.grid = grid

    # Construct a string representing a state.

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + self.d + ")"

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        return self.x+(self.grid.xmax+1)*self.y

    # Equality for states

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.d == other.d)

    # All successor states of a state

    def successors(self):
        # print("current state = ",end='')
        # print(self.__hash__())
        returnedList = []
        forward, right, left, back = self.setMoves()
        if (self.testMove(forward) or self.testMove(right) or self.testMove(left)):
            if (self.testMove(forward)):
                print("can go forward")
                nextState = self.getNextState(forward)
                returnedList.append(("forward", nextState))
            if (self.testMove(right)):
                print("can turn on the right")
                returnedList.append(("right", self.getNextState(right)))
            if (self.testMove(left)):
                print("can turn on the left")
                returnedList.append(("left", self.getNextState(left)))
        else:
            nextState = self.getNextState(back)
            returnedList.append(("back", self.getNextState(back)))
            print("have to go back")
        # print("returnedList = ")
        # print(returnedList)
        return returnedList
# Implement this function (mine is 67 lines, w/ 4 aux functions)

    def setMoves(self):
        if self.d == "N":
            return (0, 1), (1, 0), (-1, 0), (0, -1)
        if self.d == "E":
            return (1, 0), (0, -1), (0, 1), (-1, 0)
        if self.d == "S":
            return (0, -1), (-1, 0), (1, 0), (0, 1)
        if self.d == "W":
            return (-1, 0), (0, 1), (0, -1), (1, 0)

    def testMove(self, dir):
        dx, dy = dir[0], dir[1]
        # print("dx, dy = ",end='')
        # print(dx, dy)
        if (not PacManGrid.occupied(self.grid, self.x+dx, self.y+dy)):
            # print("empty cell ", end='')
            # print(getMove(dir))
            return True
        else:
            # print("wall cell ", end='')
            # print(getMove(dir))
            return False

    def getNextState(self, dir):
        if (dir != 0):
            dx, dy = dir[0], dir[1]
            nextState = PacManState(self.x, self.y, self.d, self.grid)
            nextState.x += dx
            nextState.y += dy
            nextState.d = getMove(dir)
        # print("nextState = " + nextState.__repr__())
        return nextState


def getMove(dir):
    if dir == (0, 1):
        return "N"
    if dir == (1, 0):
        return "E"
    if dir == (0, -1):
        return "S"
    if dir == (-1, 0):
        return "W"

# You can come up with your own names for the different moves
