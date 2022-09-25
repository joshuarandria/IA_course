Markov Chain Warm up
--------------------

In this exercise you will implement a very simple two state Markov Chain. The model is described in the file `doc/TwoStateMachine.pdf`.

Instructions
^^^^^^^^^^^^
1. Read `doc/TwoStateMachine.pdf`
2. Copy the file `template-twostatemachine.py` to `twostatemachine.py`
3. Read and understand the code

   - mdp.py :: This file defines an abstract class providing a general interface
     for Markov Decision Processes. No need to edit.
   - twostatemachine.py :: This defines a class implementing the simple
     machine described in `doc/TwoStateMachine.pdf`

Tasks
^^^^^
1. TASK 1.1 - Complete the rewards dictionary.
2. TASK 1.2 - Complete the probabilities dictionary.
3. TASK 1.3 - Complete the `successor_states` method.

The tasks are highlighted by `TASK` comments. Find them and more instructions in the code.

Testing
^^^^^^^

- `python twostatemachine.py` :: a basic example of usage
- `python test_twostatemachine.py` :: runs a few unit tests.

Good luck!
