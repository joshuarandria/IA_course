cComputing Conditional Probabilities & Reasoning with Bayesian Networks
----------------------------------------------------------------------
In this exercise you will write some code to estimate CPTs and also to evaluate queries given variable dependencies given as Bayesian Networks.

Instructions
^^^^^^^^^^^^
1. The python package numpy (https://numpy.org/) is needed for this exercise. If it is not already installed on your computer you can install get with `pip install numpy` (or via python distribution managers such as conda/miniconda).
2. Copy the file `template-cpt.py` to `cpt.py`
3. Read and understand the code
   - `cpt.py` Contains functions for CPT and Bayesian Network queries
   - `network.py` Contains classes for Bayesian Network and Node
   - Other files
     - 'test_cpt.py` Test code
     - Directory `data` contains test data (no need to read to complete the task)
4. Review the MyCourses material on Bayesian Networks and Inference

Tasks
^^^^^
There are four sub-tasks in this exercise, all marked with TASK in the file `cpt.py`.

1. Implement TASK 1.1 - calculate conditional probability
2. Implement TASK 1.2 - build a conditional probability table
3. Implement TASK 2.1 - exhaustive enumeration in Bayesian Networks
4. Implement TASK 2.2 - sampling in Bayesian Networks

TASK 1.1 and TASK 1.2 is about estimating
conditional probabilities given a data set as input. The Python
program, can be used
to answer probabilistic queries about the data set.
Moreover, these functions can be used to construct Bayesian Networks.

TASK 2.1 and TASK 2.2 concerns the evaluation of
probabilistic queries given a data set and the dependencies between
the variables in terms of a Bayesian network. Two methods are to be
implemented: one based on *exhaustive enumeration* of cases and the
other based on *sampling*.

Testing
^^^^^^^
`python test_cpt.py` : Will run the code on a sample data set and compare it to pre-calculated values in a unit testing framework.


Good luck!
