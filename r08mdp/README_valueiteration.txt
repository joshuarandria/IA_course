Implement value iteration
-------------------------
In this exercise you will implement the value iteration algorithm for Markov Decision Processes.

The value iteration algorithm is applied to a 2D grid decision process, where different locations on a can contain different rewards. The purpose is to compute the value of each location, and the
corresponding policy.

Instructions
^^^^^^^^^^^^
1. To prepare for the exercise, make sure you have consulted the lecture slides
and MyCourses material related to Markov Processes, The Bellman Equation, and
Value Iteration.
2. Copy `template-valueiteration.py` to `valueiteration.py`
3. Read and understand all code

   - mdp.py :: This file defines an abstract class providing a general interface
     for Markov Decision Processes. No need to edit.
   - valueiteration.py :: Declares function related to value iteration
     TASKs 2.x are found here.
   - gridmdp.py :: This file defines a grid Markov Decision Process by
     inheriting from mdp.py. No need to edit.
   - gridactions.py :: Defines actions used by gridmdp.py. No need to edit.
   - utils.py :: Defines some utility function, notably `argmax` which may come in handy.
   
4. Implement TASK 2.1, and 2.2

Tasks
^^^^^
- TASK 2.1 :: Implement the `value_of` function.
- TASK 2.2 :: Implement the `value_iteration` function (using `value_of`)

Testing
^^^^^^^
- `python valueiteration.py` :: Will execute a few basic examples on grids.
- `python test_valueiteration.py` :: Will execute a few unit tests.

Good luck!
