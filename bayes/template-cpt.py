"""
Operations to construct CPT tables and Bayes networks.
"""
# Don't modify the imports, extra imports will be removed
import itertools
import numpy
from data.mapping import * 
from network import *

# Returns number of data-rows where the rows have value specified by features
def get_data_frequency(data, features):
    """
    Returns number of rows in `data` where the rows have value specified by `features`.

    Counts all rows where for which the column values corresponds those given in `features`.
    
    Parameters
    ----------
    data : numpy array
       N x D table of recorded occurrences
    features : dict of {int : int}
       Dictionary of (data_index : value) pairs
       Key is the feature index, and value is a truth value: 0 or 1.

    Returns
    -------
    int in [0,N]
       Number of samples with corresponding feature values.
    """
    return len([item for item in data if all(item[feature] == val for feature, val in features.items())])

# Get conditional probability for given query
def get_conditional_probability(data, query, condititions):
    """
    Get conditional probability for given query.

    Calculates P(A | B ... Z) as P(A & B & ... & Z) / P (B & ... & Z).
    Here A is described by `query` and B..Z by `conditions`.

    Parameters
    ----------
    data : numpy array
       N x D table of recorded occurrences
    query : dict of {int : int}
       Features which we want to get the probability of.
       Key is the feature index, and value is a truth value: 0 or 1.
    conditions : dict of {int : int}
       Features describing the conditional part.
       Key is the feature index, and value is a truth value: 0 or 1.
    
    Returns
    -------
    float in [0,1]
       Probability of P(A | B...Z) = P(A & B & ... & Z) / P(B & ... & Z)
    """
    epsilon = 10e-5
    # Dictionary with query A and conditions B...Z
    combined_dictionary = query.copy()
    combined_dictionary.update(condititions)
    # =========================================================
    # TASK 1.1
    #  - Calculate P(A | B...Z)
    # TODO: student
    #  1. Return |data(query & conditions)| / (|data(conditions)| + epsilon)
    #  - you can use get_data_frequency(..) 
    # =========================================================
    # CODE HERE! DON'T FORGET TO RETURN SOMETHING ELSE THAN 0!
    return 0
    # =========================================================

# Construct a CPT based on query and list of conditional variables
def construct_probability_table(data, query, conditions):
    """
    Construct a CPT based on query and list of conditional variables.
    
    Go over possible assignments for condition-variables and calculate 
    conditional probability for query variable.
    
    Parameters
    ----------
    data : numpy array
       N x D table of recorded occurrences
    query : int
       ID for the variable/feature.
    conditions : list of int
       The conditions (as feature indices) for which the table should be 
       constructed. In essence the column names of the table.

    Returns
    -------
    dict of {str : float}
       Mapping from string describing the feature assignment to probability.
    """
    A = {query : 1}
    result = {}
    
    # List of all ways for assigning binary numbers to the conditions
    assignments = list(itertools.product([0, 1], repeat=len(conditions)))
    
    # Loop over all assignments of binary variables
    for assignment in assignments:
        # construct dictionary of (condition:assignment) pairs
        B = dict(zip(conditions, list(assignment)))
        # USE THIS KEY TO STORE RESULTS TO DICTIONARY
        dict_key = "vals"
        dict_key += "".join([".{}:{}.".format(key, B[key]) for key in sorted(B.keys())])
        # =========================================================
        # TASK 1.2
        #  - Construct a dictionary where 
        #       - keys are assignments of condition variables (key is provided) 
        #       - values are the conditional probabilities P(query|key)
        # 
        # TODO: student
        #  1. Calculate the conditional probability for the current assignment of variables: B
        #     - You can use get_conditional_probability(...)
        #  2. Store the probability to result dictionary with key: dict_key
        # =========================================================
        # CODE HERE! Don't forget to update `result` dictionary!
        # =========================================================
    return result

# Evaluate probability P(query = val | conditions)
def evaluate_node(G, query, val, conditions):
    """
    Evaluate probability P(query = val | conditions) given Bayesian Network.
    
    Parameters
    ----------
    G : Network (see network.py)
       The Bayesian network to base evaluation on.
    query : int
       Feature index.
    val : int
       Truth value: 0 or 1.
    conditions : dict of {int : int}
       Features describing the conditional part.
       Key is the feature index, and value is a truth value: 0 or 1.
    
    Returns
    -------
    float in [0,1]
       The probability P(query = val | conditions)
    """
    return G.get_node_probability(query, conditions) if val == 1 else 1 - G.get_node_probability(query, conditions)

# Get all variables of G in topological order
def get_topological_order(G):
    """
    Use BFS to find the order of variables in a network.

    Parameters
    ----------
    G : Network (see network.py)
       The Bayesian network for which to calculate the order.

    Returns
    -------
    list of int 
       Features as node ID's (see network.py)
       Topological order of nodes in `G`.
    """

    # Use BFS to find the order of variables in the network
    queue = G.roots[:]
    visited = set()
    for root in queue:
        visited.add(root.data_id)
    X = []
    while queue:
        node = queue.pop(0)
        X.append(node.data_id)
        for new_node in node.children:
            if new_node.data_id not in visited and all(n in visited for n in new_node.parents):
                visited.add(new_node.data_id)
                queue.append(new_node)
    return X

# Calculate probability distribution by brute force exhaustive enumerating
def exhaustive_enum(G, X, E, e):
    """
    Calculate probability distribution by brute force exhaustive enumerating
    
    Parameters
    ----------
    G : Bayesian Network (see network.py)
       The Bayesian network for which to calculate the order.
    X : list of int
       Ordered list of all features (node id's) in G.
    E : list of int
       List of features with fixed values (a subset of `X`).
    e : list of int
       Index-to-index corresponding list of values for the features in `E`.
       The values are truth values: 0 or 1.

    Returns
    -------
    float
       Sum (over all possible assignments) of the product of
       P(node | parents(node) over all nodes in G.

    """
    total = 0
    fixed_dictionary = dict(zip(E, e))
    # Make all assignments for non-fixed terms
    free_variables = [val for val in X if val not in E]
    assignments = list(itertools.product([0, 1], repeat=len(free_variables)))

    # Go over the assignments and calculate network product for each of them
    # Look for: Exhaustive Enumeration in MyCourses.
    for assignment in assignments:
        # Create a combined dictionary of assignment to free variables and fixed variables
        free_dictionary = dict(zip(free_variables, list(assignment)))
        combined_dictionary = fixed_dictionary.copy()
        combined_dictionary.update(free_dictionary)
 
        tmp = 1
        # Calculate product of probabilities in G given the assignment
        for node in G.nodes:
            # =========================================================
            # TASK 2.1: From exhaustive enumeration in the MyCourses material.
            #  - Calculate product for all probabilities over all of the nodes 
            # TODO: student
            #  1. Calculate probability P(node | parents(node)) and accumulate a product over nodes
            #    - You can use evaluate_node(...) 
            #       - If you pass all current conditions to the method, the excess ones are cut out 
            #  2. accumulate the sum once final product is calculated
            #  3. Return the complete sum
            # 
            #  HINTS: 
            #   - See exhaustive enumeration in MyCourses material.
            #   - combined dictionary consists of (node:binary) assignments
            # =========================================================
            # CODE HERE!
            # =========================================================
    return total

# Calculate distribution P(targets | e) by brute force search over the hidden variables y
def brute_force(G, targets, E, e):
    """
    Calculate distribution P(targets | e) by brute force search over the hidden variables.

    Parameters
    ----------
    G : Bayesian Network (see network.py)
       The Bayesian network for which to calculate the order.
    targets : list of int
       List of features which the distribution should be calculated over (a 
       subset of the topological order of G).
    E : list of int
       List of features with fixed values (a subset of `X`).
    e : list of int
       Index-to-index corresponding list of values for the features in `E`.
       The values are truth values: 0 or 1.

    Returns
    -------
    float
       P(targets | e)
    """

    # Get all variables of G
    X = get_topological_order(G)
    # Calculate probabilities over the possible assignments to target variables
    # one where targets are assigned to 1 and one when targets are assigned to 0
    pos = exhaustive_enum(G, X, E + targets, e + [1 for _ in range(len(targets))])
    neg = exhaustive_enum(G, X, E + targets, e + [0 for _ in range(len(targets))])
    # Return a normalized probability
    return pos / (pos + neg + + 1e-10)


# Generates random assignment of X based on E
def sample(G, X, E, e):
    """
    Generates random assignment of all Graph terms `X` based on fixed terms `E`.

    Parameters
    ----------
    G : Bayesian Network (see network.py)
       The Bayesian network for which to calculate the order.
    X : list of int
       Ordered list of all features (node id's) in G.
    E : list of int
       List of features with fixed values (a subset of `X`).
    e : list of int
       Index-to-index corresponding list of values for the features in `E`.
       The values are truth values: 0 or 1.

    Returns
    -------
    pair of (list of int, float)
       The first item of the pair is a list of truth values (0 or 1) denoting
       the truth assignment for the values of the features in `X`.
       The second is a float denoting the corresponding weight for this 
       particular assignment.

    """
    variables = []
    assignment = []
    w = 1
    
    # Algorithm Sample(..) in the MyCourses material.
    for variable in X:
        parents = dict(zip(variables, assignment))
            # =========================================================
            # TASK 2.2: complete the algorithm as in algorithm SAMPLE(..) in the MyCourses material.
            #
            # TODO: student
            #  1. If variable: var is in list E
            #     - assign: var = e[var]
            #     - update: w = w * P(var = e[var] | parents(var))
            #     
            #  2. If variable: var is not in list E
            #     - calculate prob = P(var = True | parents(var))
            #     - Generate: y = random([0, 1)) (you can use numpy.random.random)
            #     - if y < prob assign var to 1, else assign var to 0
            #
            #  3. always store variables and assignments
            #
            #  - Use G.get_node_probability(query, parents) to get P(query | parents(query))
            #    - Inputs: query = variable id, parents = dictionary of (parent_id : 0|1 )
            #    - You can pass all current assignments as parents(query) and Bayes network will ignore irrelevant variables
            # =========================================================
        if variable in E:
            # Get the fixed value for variable in e
            index = numpy.where(numpy.array(E) == variable)[0][0]
            value = e[index]
            # =========================================================
            # CODE HERE
            # =========================================================
        else:
            # =========================================================
            # CODE HERE
            # =========================================================
    return assignment, w

# Approximate a joint distribution of targets
def approximate_distribution(G, targets, E, e):
    """
  Approximate a joint distribution of features listed in `targets`.

    Parameters
    ----------
    G : Bayesian Network (see network.py)
       The Bayesian network for which to calculate the order.
    targets : list of int
       List of variables (features) that we want to calculate distribution over
    E : list of int
       List of features with fixed values.
    e : list of int
       Index-to-index corresponding list of values for the features in `E`.
       The values are truth values: 0 or 1.

    Returns
    -------
    float
       Approximated probability P(targets|e).
    """

    N = 2000
    pos_weight = 0
    total_weight = 0
    X = get_topological_order(G)

    # Make mapping of targets to X for checking when all target variables are true
    query_mapping = [X.index(target) for target in targets]

    for _ in range(N):
        tmp, w = sample(G, X, E, e)
        # Accumulate the sum only when all variables in distribution are true
        if len(tmp) > 0 and all(tmp[mapping] == 1 for mapping in query_mapping):
            pos_weight += w
        total_weight += w
    return pos_weight/(total_weight+1e-10)
