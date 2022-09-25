"""
This module contains functions used to perform the value iteration algorithm
on markov descision processes implemented using the class mdp.MDP (see mdp.py)

The function `value_iteration` performs the value iteration steps on a 
descision process until the sensitivity condition given by epsilon is met
and returns a dictionary from states to values.

The function `make_policy` returns a policy (a dictionary from states to actions)
given a process, and set of values (as computed by the value_iteration function).

The function `value_of` is a helper function calculating the sum over all successor
states given a process, and a start state and action of this process.
Used in both `value_iteration` and `make_policy`.

The function `argmax` is a helper function, giving the key with maximum value for a 
dictionary.

The parameter `mdp` is an instance of a class deriving from mdp.MDP.

The parameter `gamma` is always the discount factor and a float value.

"""

from utils import argmax

def value_of(mdp, s, a, v, gamma):
    """
    Compute the value of taking action `a` in state `s` in `mdp` with respect existing values in `v`.

    Should, given state $s$, action $a$, and discount factor $\gamma$ compute 
    $\sum_{s' \in S} P(s,a,s') * ( R(s,a,s') + \gamma * v(s') )$
    where $S$ is the set of successor states to $s$ and $a$.

    Parameters
    ----------
    mdp : mdp.MDP
    s : state
    a : action
    v  : dict of state : float
       value of states at time t - 1
    gamma : float in ]0,1[

    Returns
    -------
    float
       New value.
    """

    # -------- TASK 2.1 --------------------------------------------------------
    # TASK: Implement the function computing the sum described above and return
    # the value as a float. Look at the documentation for mdp.MDP to see how
    # the rewards R and probabilities P can be retrieved.
    #
    # CODE HERE CODE HERE CODE HERE
    pass
        
def value_iteration(mdp, gamma, epsilon = 0.001):
    """
    Perform value iteration of Markov Descision Process MDP.
    
    Parameters
    ----------
    mpd : mdp.MPD object
       Markov Descision Process
    gamma : float > 0
       Discount factor
    epsilon : float > 0
       Algorithm sensitivity.
    
    Returns
    -------
    dict of state : float
       Map from state to value, where state is in mdp.states.
    """
    # -------- TASK 2.2 --------------------------------------------------------
    # TASK: Implement the value iteration algorithm
    # This corresponds to step 1 - 3 of the algorithm as described on the
    # MyCourses pages
    # The initial value for each state is 0.
    # The return value, v, should be a dictionary mapping from states
    # to values. This corresponds to v_{n+1} once the change is small
    # enough in step 3 and the algorithm terminates.
    #
    # CODE HERE CODE HERE CODE HERE
    #
    pass
    
def make_policy(mdp, optimal_values, gamma):
    """
    Compute policy given optimal values for all states.

    Parameters
    ----------
    mdp : mdp.MDP
       Markov descision process object derived from class mdp.MDP.
    optimal_values : dict of state : value
       Optimal values, v, as e.g. computed by value_iteration.
    gamma : float in ]0,1[

    Returns
    -------
    dict of state : action
       Where state in mdp.states().
    """
    return {s1 : argmax({a : value_of(mdp, s1,a, optimal_values, gamma)
                         for a in mdp.applicable_actions(s1)})
            for s1 in mdp.states()}

if __name__ == "__main__":
    # Very basic examples.
    #
    # For more and tests with automatic compariason run test_valueiteration.py

    from gridmdp import GridMDP
    from utils import *
    
    print("--- Example 1 ------------------")
    # Walls around the sides, one large reward flanked by
    # two negative.
    gdp = GridMDP(["-*-#",
                   "...#",
                   "...#",
                   "####"],
                  tile_rewards = {'*':20, '-':-1})

    print("Input GridMDP:")
    print(gdp)

    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp,v,gamma)

    print("----------")
    print("policy:")
    visualize_policy(gdp,pi)
    print("----------")
    show_table(gdp,v,pi)
    print(
"""
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0) 	 | Value: 89.2336695350973 	 | Policy: East
Location: (0, 1) 	 | Value: 94.99586216641826 	 | Policy: Remain
Location: (0, 2) 	 | Value: 89.2336695350973 	 | Policy: West
Location: (1, 0) 	 | Value: 68.7306469062271 	 | Policy: North
Location: (1, 1) 	 | Value: 87.79342772478769 	 | Policy: North
Location: (1, 2) 	 | Value: 68.73064690622712 	 | Policy: North
Location: (2, 0) 	 | Value: 53.330846282452406 	 | Policy: North
Location: (2, 1) 	 | Value: 64.71990158234016 	 | Policy: North
Location: (2, 2) 	 | Value: 53.330846282452406 	 | Policy: North
""")
    print("--- Example 2 ------------------")
    gdp = GridMDP(["...+",
                   ".#.-",
                   "...."])
    print("Input GridMDP:")
    print(gdp)
    gamma = 0.8
    epsilon = 0.01
    v = value_iteration(gdp, gamma, epsilon)
    pi = make_policy(gdp,v,gamma)
    print("----------")
    print("policy:")
    visualize_policy(gdp,pi)
    print("----------")
    show_table(gdp,v,pi)
    print(
"""
CORRECT VALUES (Policy may differ if multiple actions has the same value)
Location: (0, 0) 	 | Value: 2.171799230512826 	 | Policy: West
Location: (0, 1) 	 | Value: 1.5086110048886463 	 | Policy: East
Location: (0, 2) 	 | Value: 2.171799230512826 	 | Policy: East
Location: (0, 3) 	 | Value: 1.7473266922805086 	 | Policy: North
Location: (1, 0) 	 | Value: 1.4798121157578978 	 | Policy: North
Location: (1, 2) 	 | Value: 1.4798121157578978 	 | Policy: North
Location: (1, 3) 	 | Value: 2.1548213018201268 	 | Policy: North
Location: (2, 0) 	 | Value: 1.692036224416641 	 | Policy: West
Location: (2, 1) 	 | Value: 1.2359387348647974 	 | Policy: South
Location: (2, 2) 	 | Value: 1.6920362244166411 	 | Policy: East
Location: (2, 3) 	 | Value: 2.1887771592055256 	 | Policy: South
""")
    
    print("--- Example 3 ------------------")
    print("Example using a basic two-state machine.")
    
    from twostatemachine import TwoStateMachine
    tsm = TwoStateMachine()
    gamma = 0.5
    epsilon = 0.01
    vi = value_iteration(tsm, gamma, epsilon)
    va = tsm.analytic(gamma)
    print("""(using gamma = {0}, epsilon = {1})

Iterated values 
---------------
upright: {2}
prone  : {3}

Theoretical values
------------------
upright: {4}
prone  : {5}

""".format(gamma,epsilon,
           vi[TwoStateMachine.States.upright],
           vi[TwoStateMachine.States.prone],
           va[TwoStateMachine.States.upright],
           va[TwoStateMachine.States.prone]
           ))
    


