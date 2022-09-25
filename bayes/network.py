"""
Bayesian Network and Node classes.
"""
from cpt import construct_probability_table

# Bayes network construction
class Network:
    """
    Describes a Bayesian network

    Attributes
    ----------
    data : numpy array
       N x D table of recorded occurrences
    nodes : list of Node objects
       The nodes of the network
    roots : list of Node objects
       The subset of nodes without parents
    """

    def __init__(self, data):
        """
        Initialize network

        Parameters
        ----------
        data : numpy array
           N x D table of recorded occurrences
        
        """
        self.nodes = []
        self.roots = []
        self.data = data

    def get_node(self, feature):
        """
        Look for a unique node with specific feature in network.

        Returns the node with attribute `data_id` equal to parameter `feature`,
        if the node exists in the network, and it is unique.

        Parameters
        ----------
        feature : int
           The feature id to compare to the nodes' `data_id` attribute.

        Returns
        -------
        Node object or None
           Node if it exists and is unique, None otherwise.
        """
        res = [node for node in self.nodes if node.data_id == feature]
        return res[0] if len(res) == 1 else None

    # Method to get P(feature | conditions)
    def get_node_probability(self, feature, conditions):
        """
        Compute P(feature | conditions).

        Parameters
        ----------
        feature : int
           node_id for the query 
        conditions : dict of int : bool
           The conditional probabilities as mapping from node_id (feature)
           to truth value.

        Returns
        -------
        float in [0,1]
           The probability.
        """
        node = self.get_node(feature)
        tmp = {}

        # Get rid of excess parent-conditions
        for key in conditions.keys():
            if key in node.parents:
                tmp[key] = conditions[key]
        
        # We can only evaluate node which has assignment to all of it's parents
        assert len(tmp) == len(node.parents), "Not all parents of a node have a value"

        # Make a key
        dict_key = "vals" # + str(B)
        dict_key += "".join([".{}:{}.".format(key, tmp[key]) for key in sorted(tmp.keys())])
        return node.probabilities[dict_key]

    def append_node(self, node_id, name, parents = []):
        """
        Creates a new node in the network.
        
        Parameters
        ----------
        node_id : int
           The id of node to add.
        name : str
           Human-readable name of node being added.
        parents : list of Node objects
           The node's parents already in the network.

        Raises
        ------
        AssertionError
           If a node's parent is not a member of the network.
        """
        node = Node(name, node_id)
        node.probabilities = construct_probability_table(self.data, node_id, parents)

        node.parents = parents
        self.nodes.append(node)
        if parents != []:
            for parent in parents:
                res = self.get_node(parent)
                assert res != None
                res.children.append(node)
        else:
            self.roots.append(node)


# A node in Bayes network
class Node:
    """
    A node in a Bayes network.

    Attributes
    ----------
    node_id : int
       The id of node to add. A.k.a. 'feature'.
    name : str
       Human-readable name of Node.
    parents : list of Node objects
       The node's parent Nodes.
    children: list of Node objects
       The node's child Nodes.
    probabilities: dict of str : float
       Mapping from unique feature truth assignment for all parents and Node
       to probability.
  
    """
    def __init__(self, name, node_id):
        """
        Initialize node

        Parameters
        ----------
        name : str
           Human-readable name of node being added.
        node_id : int
           The id of node to add.
        """
        self.name = name
        self.data_id = node_id
        self.probabilities = []
        self.parents = []
        self.children = []

    def add_parent(self, parent):
        """
        Add `parent` as a parent of current Node.

        Parameters
        ----------
        parent : Node
           The parent node.
        """
        self.parents.append(parent)
        
    def add_child(self, child):
        """
        Add `child` as a child of current Node.

        Parameters
        ----------
        child : Node
           The child node.
        """
        self.children.append(child)


