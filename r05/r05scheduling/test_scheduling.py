import unittest
from unittest.mock import patch
from scheduling import at_most_one, at_least_one, problem_to_formula, variable
from scheduling import exactly_one_execution, mutually_exclusive_tasks, task_ordering
from logic import ATOM, AND, OR, NOT, IMPL, EQVI
from z3_wrapper import solve, Bool
from random import seed


seed(0)
def var(task, time_slot):
    return Bool(variable(task, time_slot).name)


def scheduling_problem_from_the_slides():
    return {"tasks": ["1R", "1B", "1G", "2R", "2B", "2G", "3R", "3B", "3G"],
            "orders": [("1R", "1B"), ("1B", "1G"), ("2B", "2G"), ("2G", "2R"), ("3B", "3R"), ("3R", "3G")],
            "resource_need": {"1R": "Red", "2R": "Red", "3R": "Red", "1G": "Green", "2G": "Green", "3G": "Green", "1B": "Blue",
                              "2B": "Blue", "3B": "Blue"},
            "time_horizon": 5}


def scenario_two():
    return {"tasks": ["1R", "1B", "1G", "2R", "2B", "2G", "3R", "3B", "3G", "4R", "4B", "4G", "5R", "5B", "5G"],
            "orders": [("1B", "1R"), ("1R", "1G"), ("2R", "2G"), ("2G", "2B"), ("3R", "3B"), ("3B", "3G"), ("4B", "4R"),
               ("4R", "4G"), ("5R", "5B"), ("5B", "5G")],
            "resource_need": {"1R": "Red", "2R": "Red", "3R": "Red", "1G": "Green", "2G": "Green", "3G": "Green", "1B": "Blue",
                              "2B": "Blue", "3B": "Blue", "4R": "Red", "5R": "Red", "6R": "Red", "4G": "Green", "5G": "Green",
                              "4B": "Blue", "5B": "Blue", "6B": "Blue"},
            "time_horizon": 7}


def scenario_three():
    return {"tasks": ["1R", "1B", "1G", "2R", "2B", "2G", "3R", "3B", "3G", "4R", "4B", "4G", "5R", "5B", "5G", "6R", "6B", "6G"],
            "orders": [("1R", "1B"), ("1B", "1G"), ("2B", "2G"), ("2G", "2R"), ("3B", "3R"), ("3R", "3G"), ("4R", "4B"), ("4B", "4G"),
                       ("5B", "5G"), ("5G", "5R"), ("6B", "6R"), ("6R", "6G")],
            "resource_need": {"1R": "Red", "2R": "Red", "3R": "Red", "1G": "Green", "2G": "Green", "3G": "Green", "1B": "Blue",
                              "2B": "Blue", "3B": "Blue", "4R": "Red", "5R": "Red", "6R": "Red", "4G": "Green", "5G": "Green",
                              "6G": "Green", "4B": "Blue", "5B": "Blue", "6B": "Blue"},
            "time_horizon": 8}


def scenario_four():
    return {"tasks": ["1R", "1B", "1G", "2R", "2B", "2G", "3R", "3B", "3G", "4R", "4B", "4G", "5R", "5B", "5G", "6R", "6B",
                      "6G", "7R", "7B", "7G"],
            "orders": [("1B", "1G"), ("1G", "1R"), ("2G", "2R"), ("2R", "2B"), ("3B", "3G"), ("3G", "3R"), ("4B", "4R"),
                       ("4R", "4G"), ("5B", "5R"), ("5R", "5G"), ("6G", "6B"), ("6B", "6R"), ("7R", "7B"), ("7B", "7G")],
            "resource_need": {"1R": "Red", "2R": "Red", "3R": "Red", "1G": "Green", "2G": "Green", "3G": "Green", "1B": "Blue",
                              "2B": "Blue", "3B": "Blue", "4R": "Red", "5R": "Red", "6R": "Red", "7R": "Red", "4G": "Green",
                              "5G": "Green", "6G": "Green", "7G": "Green", "4B": "Blue", "5B": "Blue", "6B": "Blue", "7B": "Blue"},
            "time_horizon": 7}


class MyTestCase(unittest.TestCase):
    def check_exactly_one_execution(self, tasks, time_horizon):
        formula = exactly_one_execution(tasks, (1, time_horizon + 1))
        result, model, _ = solve(formula)
        # print(model)
        self.assertTrue(result, "\nError: exactly_one_execution) the formula is not satisfiable")
        plan = {}
        for task in tasks:
            for time in range(1, time_horizon + 1):
                if model[var(task, time)]:
                    self.assertFalse(task in plan, f"\nError: exactly_one_execution) the task \"{task}\" executed more than one time!")
                    plan[task] = time
            self.assertTrue(task in plan, f"\nError: exactly_one_execution) the task \"{task}\" has not scheduled!")

    def check_mutually_exclusive_tasks(self, tasks, resource_need, time_horizon):
        formula = mutually_exclusive_tasks(tasks, resource_need, (1, time_horizon + 1))
        result, model, _ = solve(formula)
        self.assertTrue(result, "\nError: mutually_exclusive_tasks) the formula is not satisfiable")
        available_resources = {resource: [True for _ in range(time_horizon)] for _, resource in resource_need.items()}
        for task in tasks:
            for time in range(time_horizon):
                if model[var(task, time + 1)]:
                    self.assertTrue(available_resources[resource_need[task]][time],
                                    f"\nError: mutually_exclusive_tasks) the resource \"{resource_need[task]}\" is used by at least two tasks,"
                                    f"at time step: {time + 1}")
                    available_resources[resource_need[task]][time] = False

    def check_task_ordering(self, tasks, orders, time_horizon):
        formula = task_ordering(orders, (1, time_horizon + 1))
        result, model, _ = solve(formula)
        self.assertTrue(result, "\nError: task_ordering) the formula is not satisfiable")
        execution = {}
        for task in tasks:
            for time in range(1, time_horizon + 1):
                if model[var(task, time)]:
                    execution.setdefault(task, []).append(time)

        for (task_1, task_2) in orders:
            for time_1 in execution.get(task_1, []):
                for time_2 in execution.get(task_2, []):
                    self.assertLess(time_1,
                                    time_2,
                                    f"\nError: task_ordering) the ordering constraint for tasks \"{task_1}\" and \"{task_2}\" is not met!")


    def check(self, tasks, orders, resource_need, time_horizon):
        # self.check_exactly_one_execution(tasks, time_horizon)
        # self.check_mutually_exclusive_tasks(tasks, resource_need, time_horizon)
        self.check_task_ordering(tasks, orders, time_horizon)

    #     formula = problem_to_formula(tasks, orders, resource_need, time_horizon)
    #     result, model, _ = solve(formula)
    #     self.assertTrue(result, "\nError: problem_to_formula) The encoded formula should be satisfiable!")

    # def test_at_least_one(self):
    #     time_steps = range(20)
    #     task = "Test_Task"
    #     formula = at_least_one([variable(task, time) for time in time_steps])
    #     result, model, _ = solve(formula)
    #     self.assertTrue(result, "\nError: at_least_one) The formula is not satisfiable")
    #     true_elements = sum([1 if model[var(task, time)] else 0 for time in time_steps])
    #     self.assertLessEqual(1, true_elements, "\nError: at_least_one) No elements is true!")

    # def test_at_most_one(self):
    #     time_steps = range(20)
    #     task = "Test_Task"
    #     formula = at_most_one([variable(task, time) for time in time_steps])
    #     result, model, _ = solve(formula)
    #     self.assertTrue(result, "\nError: at_most_one) The formula is not satisfiable")
    #     true_elements = sum([1 if model[var(task, time)] else 0 for time in time_steps])
    #     self.assertGreaterEqual(1, true_elements, "\nError: at_most_one) More than one elements is true!")

    def test_scheduling_problem_from_slides(self):
        self.check(**scheduling_problem_from_the_slides())

    # def test_scenario_two(self):
    #     self.check(**scenario_two())

    # def test_scenario_three(self):
    #     self.check(**scenario_three())

    # def test_scenario_four(self):
    #     self.check(**scenario_four())

    @staticmethod
    def show_the_scheduling(model, tasks, time_horizon):
        """
        Shows the solution for the scheduling problem

        Parameters
        ----------
        model: Dict[str, bool] or Dict[z3.Bool, bool]
            A dictionary that maps variables to their truth-values.
            If we used our DPLL, then its type is: Dict[str, bool].
            Otherwise, if we used Z3, then its type is:
            Dict[z3.Bool, bool]
        tasks: List[str]
            A list of strings representing the tasks to be scheduled
        time_horizon: int
            An integer which defines the time horizon (the maximum time point)
        """
        max_task_name_length = max(len(task) for task in tasks)
        result = {}
        for t in range(1, time_horizon + 1):
            print("Time {}:".format(t), end=' ')
            for task in tasks:
                if model[var(task, t)]:
                    result[task] = t
                    print(task, end=' ')
                    for a in range(len(task), max_task_name_length):
                        print("", end=' ')
            print("")
        return result

    @staticmethod
    def solve_problem(tasks, orders, resource_need, time_horizon):
        """
        Solves a scheduling problem by reduction to SAT

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
        """
        formula = problem_to_formula(tasks, orders, resource_need, time_horizon)
        result_to_string = {True: "Satisfiable", False: "Unsatisfiable"}

        result, model, z3_duration = solve(formula)
        print("result:", end=' ')
        print(result_to_string[result])
        print("search time : {}(s)".format(z3_duration))
        print("")
        if result:
            return MyTestCase.show_the_scheduling(model, tasks, time_horizon)
        else:
            return None

    # @classmethod
    # def tearDownClass(cls):
    #     print("")
    #     print("##########################################")
    #     print("Scheduling problem from the slides:")
    #     cls.solve_problem(**scheduling_problem_from_the_slides())
    #     print("##########################################")

    #     print("Scenario two:")
    #     cls.solve_problem(**scenario_two())
    #     print("##########################################")

    #     print("Scenario three:")
    #     cls.solve_problem(**scenario_three())
    #     print("##########################################")

    #     print("Scenario four:")
    #     cls.solve_problem(**scenario_four())
    #     print("##########################################")
    
if __name__ == '__main__':
    unittest.main()
