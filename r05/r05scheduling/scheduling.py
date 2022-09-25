from random import random
from time import time

from torch import randint
from logic import AND, OR, NOT, ATOM, IMPL, EQVI


def variable(task, time_slot):
    """
    Creates a Boolean variable expressing: `task` is preformed at `time_slot`

    This is just a wrapper to create a Bool variable (atom) with a string
    representing the particular `task` and `time_slot`

    Parameters
    ----------
    task: str
        Task name
    time_slot: int
        The time slot

    Returns
    -------
    ATOM
        Boolean variable (atom) to be used in formulas. If this variable is
        assigned True, it means the `task` should be performed at `time_slot`.
    """
    return ATOM("{}@{}".format(task, time_slot))


# Convention
# ----------
# In this file, we call any logical object of: `AND`, `OR`, `NOT`, and `ATOM`,
# as a `Formula`.
#
# For example:
# ```
# formula_1 = variable("Task_1", 3)
# formula_2 = NOT(variable("Task_3", 2))
# formula_3 = AND([formula_1, formula_2])
# formula_4 = OR([NOT(formula_3), formula_1, formula_2])
# ```
# All the of `formula_1`, `formula_2`, `formula_3`, and `formula_4` are objects
# of type `Formula`


# Tasks: Encoding a scheduling problem into a SAT problem
# -------------------------------------------------------------------------------
#
# Here, we encode a scheduling problem into a SAT problem. In other words, we
# should implement the constraints we have learned from the lecture, to describe
# a scheduling problem as a SAT problem.
#
#
# In the first part, we will complete some helper functions. Those functions are
# supposed to make our encoding easier.
#
# TASK 1
# ======
# There are two functions that we need to implement:
# `at_least_one`: We are given a list of formulas, and we need to create a new
#                 formula that expresses at least one formula in the list must
#                 be true.
# `at_most_one`: in this function, we are given a list of formulas, and we need
#                to create a new formula that expresses at most one formula in
#                the list must be true.
#
#
# In the second part, we encode the scheduling problem into a SAT problem:
#
# TASK 2
# ======
# In this task, we will implement three functions, each of which encodes
# a main constraint of the scheduling problem to a formula:
# `exactly_one_execution`: for a given task list, we should formulate a
#                          formula that makes each task takes place exactly
#                          once.
# `mutually_exclusive_tasks`: Each task needs a specific resource; we should
#                             not let two tasks depending on the same resource
#                             executed simultaneously.
# `task_ordering`: Additionally, executing a task may require the results of
#                  some other tasks; thus, we have to execute it only after the
#                  other one.


def all_pairs(elements):
    """
    Helper function, giving all pairs of a list of elements

    Parameter
    --------
    elements: List[Any]
        list of elements

    Returns
    -------
    List[Tuple[Any, Any]]
       Unique pairings of the elements in the given list.
    """
    return [(elements[i], elements[j]) for i in range(0, len(elements))
            for j in range(i + 1, len(elements))]


def at_least_one(formulas):
    """
    Expresses that at least one formula in the given list must be true

    Parameters
    ----------
    formulas: List[Formula]
        list of formulas

    Returns
    -------
    Formula
        An object of type `Formula` that specifies at least one formula of the
        given input evaluates to true.
    """

    # Task 1.1
    # ========
    # Please describe a formula to specify at least one of the given formulas
    # should be true.
    retFormula = OR([f for f in formulas])
    return retFormula


def at_most_one(formulas):
    """
    Expresses that at most one formula in the given list must be true.

    Parameters
    ----------
    formulas: List[Formula]
        list of formulas

    Returns
    -------
    Formula
        An object of type `Formula` that specifies at most one formula of the
        given input evaluates to true.
    """
    # Task 1.2
    # ========
    # Please describe a formula to specify at most one of the given formulas
    # should be true.
    # i=0
    # for x in all_pairs(formulas):
    #     print(AND([x[0],x[1]]))
    #     i+=1
    #     if i>5:
    #         break
    retFormula = NOT(OR([AND([x[0], x[1]]) for x in all_pairs(formulas)]))
    return retFormula
    # Tips
    # ====
    # You can use the function 'allpairs' above to get the pairing of formulas.


def exactly_one(formulas):
    """
    Expresses that exactly one formula in the given list must be true.

    Parameters
    ----------
    formulas: List[Formula]
        list of formulas

    Returns
    -------
    Formula
        An object of type `Formula` that specifies exactly one formula of the
        given input evaluates to true.
    """
    return AND([at_most_one(formulas), at_least_one(formulas)])


def exactly_one_execution(tasks, time_interval):
    """
    Expresses a formula that makes each task takes place exactly once, during
    the specified time interval

    Parameters
    ----------
    tasks: List[str]
        A list of strings representing the tasks to be scheduled
    time_interval: Tuple[int, int]
        time interval: [start time, end time).
        in other words, the time interval is between `time_interval[0]` and
        `time_interval[1]`, including `time_interval[0]`, excluding `time_interval[1]`.


    Returns
    -------
    Formula
        A formula that specifies each task takes place exactly once
    """

    # Task 2.1
    # ========
    # Please describe a formula to specify each task will be done exactly once
    # during the given time interval.

    exactFormulas = []
    for i in range(len(tasks)):
        formulasi = [variable(tasks[i], j)
                     for j in range(time_interval[0], time_interval[1])]
        # print(formulasi)
        exactFormulasi = exactly_one(formulasi)
        # print(exactFormulasi)
        exactFormulas.append(exactFormulasi)
    retFormula = AND([exactFormulas[i] for i in range(len(exactFormulas))])
    # print(retFormula)
    return retFormula
    # Tips
    # ====
    # You can use the `exactly_one` function, defined above.


def mutually_exclusive_tasks(tasks, resource_need, time_interval):
    """
    Expresses a formula to prevent the simultaneous execution of tasks needing
    the same resource.

    Parameters
    ----------
    tasks: List[str]
        A list of strings representing the tasks to be scheduled
    resource_need: Dict[str, str]
        A dictionary. `resource_need[task] = resource` means that `task`
        needs the `resource`
    time_interval: Tuple[int, int]
        time interval: [start time, end time).
        in other words, the time interval is between `time_interval[0]` and
        `time_interval[1]`, including `time_interval[0]`, excluding `time_interval[1]`.

    Returns
    -------
    Formula:
        A formula that prevents tasks with the same needing resource execute
        simultaneously.
    """
    # Task 2.2
    # ========
    # Please describe a formula to forbid the parallel execution of tasks
    # needing the same resource

    # differentResource = []
    # currentResource = resource_need[tasks[0]]
    # differentResource.append(currentResource)
    # for task in tasks:
    #     if (not(resource_need[task] in differentResource)):
    #         currentResource = resource_need[task]
    #         differentResource.append(currentResource)
    # # print(differentResource)
    formulaTab = []
    for taskPair in all_pairs(tasks):
        # print("taskPair :",end=" ")
        # print(taskPair[0],end=", ")
        # print(taskPair[1])
        if resource_need[taskPair[0]] == resource_need[taskPair[1]]:
            # print("same resource")
            for j in range(time_interval[0], time_interval[1]):
                formula = (
                    NOT(AND([variable(taskPair[0], j), variable(taskPair[1], j)])))
                formulaTab.append(formula)
            # print(formula)
            # formulaTab.append(formula)
    # print(formulaTab)
    # formulaIntermed=AND(f for f in formulaTab)
    # print(formulaTab)

    retFormula = AND([f for f in formulaTab])
    # for task in tasks:
    #     print(resource_need[task])
    #     for task in tasks:
    #     if(resource_need[task] == ):
    #         formulaRed.append(task)
    # print(formulaRed)
    # print(resource_need)
    # retFormula=AND([exactFormulas[i] for i in range (len(exactFormulas))])
    # retFormula = 0
    print(retFormula)
    return retFormula


def task_ordering(orders, time_interval):
    """
    Expresses a formula to impose our required task ordering

    Parameters
    ----------
    orders: List[(str, str)]
        A list of pairs `(task_1,task_2)`, meaning that `task_1` must
        precede `task_2`
    time_interval: Tuple[int, int]
        time interval: [start time, end time).
        in other words, the time interval is between `time_interval[0]` and
        `time_interval[1]`, including `time_interval[0]`, excluding `time_interval[1]`.

    Returns
    -------
    Formula
        A formula that specifies the task ordering
    """

    # Task 2.3
    # ========
    # Please describe a formula to specify the required task ordering
    
    formulas=[]
    for taskPair in orders:
        formulaTab = []
        for t1 in range (time_interval[0], time_interval[1]-1):
            for t2 in range(t1+1,time_interval[1]):
                formula=AND([variable(taskPair[0], t1), variable(taskPair[1], t2)])
                formulaTab.append(formula)
                print(formulaTab)
        formula2=OR([f for f in formulaTab])
        print(formula2)
        formulas.append(formula2)

    retFormula = AND([f for f in formulas])
    # retFormula = AND([exactFormulas[i] for i in range (len(exactFormulas))])
    # retFormula=0
    print(retFormula)
    return retFormula


def problem_to_formula(tasks, orders, resource_need, time_horizon):
    """
    Encodes a scheduling problem to a SAT problem

    Parameters
    ----------
    tasks: List[str]
        A list of strings representing the tasks to be scheduled
    orders: List[(str, str)]
        A list of pairs `(task_1,task_2)`, meaning that `task_1` must
        precede `task_2`
    resource_need: Dict[str, str]
        A dictionary. `resource_need[task] = resource` means that `task`
        needs the `resource`
    time_horizon: int
        An integer which defines the time horizon (the maximum time point)

    Returns
    -------
    Formula
        The encoded logical formula
    """

    time_interval = (1, time_horizon + 1)
    return AND([exactly_one_execution(tasks, time_interval),
                mutually_exclusive_tasks(tasks, resource_need, time_interval),
                task_ordering(orders, time_interval)])
