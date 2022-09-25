
#
# Construct PDB heuristics for N-Puzzle

import Npuzzle

import queue

# Breadth-First Search (uninformed)
#
# Modify the breadth-first search algorithm to record the distances of
# all state from the initial state, and to return those distances.
# It is best to use a dictionary, so that distances of state can be
# recorded as distances[s] = ... and accessed as distances[s].


def breadthFirstSearch(initialstate):

    visited = dict()  # dictionary (hash table) for holding visited states
    distances = dict()
    distances[initialstate] = 0

    Q = queue.Queue(maxsize=0)  # first-in-first-out queue

    Q.put(initialstate)  # Insert the initial state in the queue
    visited[initialstate] = 1

    maxdist = 20
    while not Q.empty():
        state = Q.get()  # Next un-expanded state from the queue
        # print("state__hash__")
        # print(state)
        # print("distance[state]")
        if distances[state] > maxdist:
            print(distances[state])
            maxdist = distances[state]
        for aname, s, cost in state.successors():  # Go through all successors of state
            if s not in visited:  # Was the state visited already?
                visited[s] = 1
                distances[s] = distances[state]+1
                Q.put(s)
            else:
                if distances[s] > distances[state]+1:
                    distances[s] = distances[state]+1
    # print(distances)
    return distances

# Construct a PDB heuristic based on a subset of tiles
#
# makePDBheuristics takes as input
#
# - the goal state to which distance is estimated
# - the set of tiles that are to be included in the PDB
#
# makePDBheuristics returns a function that
#
# - takes a state as input
# - returns a lower bound estimate for the distance to the goal state


def makePDBheuristic(goalState, tiles):
    print("heurFct computation")
    # abstractGoalState = goalState.copy()
    # abstractGoalState.show
    # abstractGoalState.abstract(tiles)
    abstractGoalState = goalState.abstract(tiles)
    # abstractGoalState.show()

    def heurFct(state):
        distances = breadthFirstSearch(abstractGoalState)
        return distances[state.abstract(tiles)]
    return lambda state: heurFct(state)


# Construct a PDB heuristics based on PDBs for two subsets of tiles
#
# This is like makePDBheuristics, except that two PDBs are constructed
# and used for deriving a lower bound distance estimate.
# Depending on whether the subsets intersect or not, the lower bounds
# from the two PDBs can be combined either by summing or by maximizing.
#
# makePDBheuristic2 return one function just like makePDBheuristic2 does.

def makePDBheuristic2(goalState, tiles1, tiles2):

    abstractGoalState1 = goalState.abstract(tiles1)
    distances1 = breadthFirstSearch(abstractGoalState1)
    abstractGoalState2 = goalState.abstract(tiles2)
    distances2 = breadthFirstSearch(abstractGoalState2)

    def heurFct2(state):
        sumOrmax = 0
        for tile in tiles1:
            if tile in tiles2:
                sumOrmax = 1
                break
        if sumOrmax == 1:
            return max(distances1[state.abstract(tiles1)], distances2[state.abstract(tiles2)])
        else:
            return distances1[state.abstract(tiles1)] + distances2[state.abstract(tiles2)]
    return lambda state: heurFct2(state)