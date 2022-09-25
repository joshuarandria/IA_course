
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

    visited = dict() # dictionary (hash table) for holding visited states
#### YOUR CODE HERE ####
        
    Q = queue.Queue(maxsize=0) # first-in-first-out queue

    Q.put( initialstate ) # Insert the initial state in the queue
    visited[initialstate] = 1
    
    while not Q.empty():
        state = Q.get() # Next un-expanded state from the queue
        for aname,s,cost in state.successors(): # Go through all successors of state
            if s not in visited: # Was the state visited already?
                visited[s] = 1
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
                Q.put( s )
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####

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

def makePDBheuristic(goalState,tiles):
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####


# Construct a PDB heuristics based on PDBs for two subsets of tiles
#
# This is like makePDBheuristics, except that two PDBs are constructed
# and used for deriving a lower bound distance estimate.
# Depending on whether the subsets intersect or not, the lower bounds
# from the two PDBs can be combined either by summing or by maximizing.
#
# makePDBheuristic2 return one function just like makePDBheuristic2 does.

def makePDBheuristic2(goalState,tiles1,tiles2):
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
#### YOUR CODE HERE ####
