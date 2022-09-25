CS-E4800 Tournament
###################

Welcome to the "CS-E4800 Tournament"!

In this tournament, we will develop an agent to play the Oware game.

The rules of the game are described here:
    * https://www.yourturnmyturn.com/rules/oware.php
    * The game also ends when it exceeds 240 turns. In this case, the winner is
      the player with the most seeds. It means the condition for the
      "endless cycle of moves" described in the rules is not valid in this
      tournament.
    * In addition to the above rules, we consider a time limit (e.g., 5 seconds)
      for each turn. As it would be difficult to adjust to any given time-bound,
      each player can generate a sequence of increasing good actions in each
      turn, and the last action within the time limit will be considered as the
      chosen action for that turn.
      If a player does not choose any action within the time limit or it
      chooses an invalid move, a random action will be selected for the
      player.


Requirements
^^^^^^^^^^^^
To run this program, we need to install `Pillow`:
` pip install Pillow==9.0.1`


Instructions
^^^^^^^^^^^^
0. (Optional) Play the game to learn and understand its rules.
   You can play the game by running the following command:
   `python3 main.py`
   The possible actions are shown by green lights at the bottom or top of the
   pits. Clicking on a pit will choose the corresponding action.

   You can play against different agents (or another human). To specify your
   opponent, you can modify the `players` variable in the `main.py`.

1. Copy `agent-template.py` to `agent.py`.

2. Read and understand the `agent.py`.

3. Take a brief look at the following agents:
3.1. the `RandomAgent` in `random_agent.py`,
3.2. the `MCSAgent` in `mcs_agent.py`,
3.3. the `MinimaxAgent` in `minimax_agent.py`,
3.4. the `IterativeDeepening` in `iterative_deepening.py`, and,
3.5. the `IDMinimaxAgent` in `id_minimax_agent.py`.

4. Complete the `info` method of the `Agent` class

5. Complete the `decide` method of the `Agent` class by developing an algorithm
   to overcome all opponents. You are free to choose what kind of game-playing 
   agent you want to implement. Some obvious approaches are the following:
5.1 Implement alpha-beta (and investigate its potential for searching deeper
    than what is possible with Minimax). Also, the order in which the actions
    are tried in a given node impacts the effectiveness of alpha-beta: you could
    investigate different ways of ordering the actions/successor states.
5.2 Try out better heuristics.
5.3 You could try out more advanced Monte Carlo search methods; however, we do
    not know whether MCTS is competitive because of the high cost of the full
    gameplays.
5.4 You could, of course, try something completely different if you are willing to
    invest more time.


Simulation
^^^^^^^^^^
For simulating the game, you can use the `main.py` script. Just import your agent
and `play` the game with an instance of your agent.


GL HF :)
