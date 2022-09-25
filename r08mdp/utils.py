from math import inf

def argmax(d):
    """
    Return key corresponding to maximum value in dictionary `d`.

    If several keys have the same maxum value, one of them will be returned.

    Parameters
    ----------
    d : dict
       values must be numeric
    
    Returns
    -------
    key in `d`
    """
    return max(d, key = lambda k : d[k])


def show_table(mdp,v,pi):
    """
    Print results as a table.
    """
    print("Computed values and policy")
    for s in sorted(mdp.states()):
        print("Location: {0} \t | Value: {1} \t | Policy: {2}".format(s, v[s], pi[s]))


def visualize_policy(mdp,pi):
    """"
    Print grid with shortcut for policy.
    """
    for r in range(mdp.n_rows):
        row_str = ""
        for c in range(mdp.n_cols):
            if (r,c) not in mdp._states:
                row_str += '#'
            else:
                row_str += str(pi[(r,c)])[0]
        print(row_str)

def follow_pi(pi,ss,gs,mdp):
    """
    Count number of actions from start state to end state for given policy.

    Deterministically follows policy by application of actions from start state to 
    the goal state or infinite loop is encountered.

    Parameters
    ----------
    pi : dict {(int,int) : GridAction}
       Policy.
    ss : (int,int) 
       Start state in `mpd`
    gs : (int,int)
       Goal state in `mdp`
    mdp : Class inheriting from MDP (see `mdp.py`).
       Markov Descision Process.
    """
    prev = set()
    s = ss
    l = 0
    while s != gs:
        ss = pi[s](s)
        l += 1
        if ss in mdp._states:
            s = ss
        if s in prev:
            return inf
        else:
            prev.add(s)
    return l

