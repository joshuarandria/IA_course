import unittest

from valueiteration import *
from twostatemachine import TwoStateMachine
from gridmdp import GridMDP

class TestValueIterationsGMP(unittest.TestCase):
    """
    Tests using GridMDP.
    """

    def test_1_value_of_return(self):
        """Check value_of returns something"""
        # Make grid with no walls and no rewards.
        gdp = GridMDP(["...",
                       "...",
                       "..."])
        # Just pick one state and action
        a = list(gdp._actions)[0]
        s = (0,0)
        # Let the values for all states be 0
        v = {s2 : 0 for s2 in gdp.states()}
        val = value_of(gdp, s, a, v, 0.5)
        # Check that it isn't None
        self.assertIsNotNone(val, msg = "Check that value_of returns a value (TASK 2.1)")
        # It needs to return a float. In this particular case it should be 0 as there are no values.
        self.assertEqual(val, 0, msg = "Check (TASK 2.1)")

    def test_2_valueiteration_return(self):
        """Check so value_iteration returns a dictionary."""
        gdp = GridMDP([".+.",
                       "-.#",
                       "#.."])
        gamma = 0.8
        epsilon = 0.01
        v = value_iteration(gdp, gamma, epsilon)
        # If value_iteration has not been implemented the return value is None.        
        self.assertIsNotNone(v, msg = "Check if value_iteration returns a value (TASK 2.2)")
        # It needs to return a dictionary.
        self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary (TASK 2.2)")
        
    # def test_3_GridMDP_1(self):
    #     """ 
    #     Test based on GridMDP and numerical accuracy.

    #     """
        
    #     gdp = GridMDP([".+.",
    #                    "-.#",
    #                    "#.."])
        
    #     gamma = 0.8
    #     epsilon = 0.01
    #     v = value_iteration(gdp, gamma, epsilon)
    #     self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
    #     # It needs to return a dictionary.
    #     self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
    #     # Correct values
    #     v_correct = {(0, 1): 1.571722060790156,
    #                  (2, 1): 1.978450493796204,
    #                  (0, 0): 1.851675645926026,
    #                  (1, 1): 1.851675645926026,
    #                  (0, 2): 1.978450493796204,
    #                  (2, 2): 1.4386906812824292,
    #                  (1, 0): 1.2307799307753424}
        
    #     for s in v:
    #         self.assertAlmostEqual(v[s],v_correct[s],
    #                                msg="Values differ for GridMDP example 1. Check value_iteration and value_of", places = 6)
            
    # def test_4_GridMDP_2(self):
    #     """ 
    #     Test based on GridMDP and numerical accuracy.
    #     """
        
    #     gdp = GridMDP(["...+",
    #                    ".#.-",
    #                    "...."])
    #     gamma = 0.8
    #     epsilon = 0.01
    #     v = value_iteration(gdp, gamma, epsilon)
    #     # If value_iteration has not been implemented the return value is None.        
    #     self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
    #     # It needs to return a dictionary.
    #     self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
    #     # Correct values
    #     v_correct = {(0, 1): 1.5086110048886463,
    #                  (1, 2): 1.4798121157578978,
    #                  (2, 1): 1.2359387348647974,
    #                  (0, 0): 2.171799230512826,
    #                  (0, 3): 1.7473266922805086,
    #                  (2, 0): 1.692036224416641,
    #                  (2, 3): 2.1887771592055256,
    #                  (0, 2): 2.171799230512826,
    #                  (2, 2): 1.6920362244166411,
    #                  (1, 0): 1.4798121157578978,
    #                  (1, 3): 2.1548213018201268}
    #     for s in v:
    #         self.assertAlmostEqual(v[s],v_correct[s],
    #                                msg="Values differ for GridMDP example 2. Check value_iteration and value_of")
        
    # def test_5_GridMDP_3(self):
    #     """ 
    #     Test based on GridMDP and numerical accuracy.
    #     """
    #     gdp = GridMDP([".......",
    #                    ".......",
    #                    "..-+*..",
    #                    ".......",
    #                    "......."],
    #             tile_rewards = {'-':-1,'+':2,'*':-9})
    #     gamma = 0.5
    #     epsilon = 0.01
    #     v = value_iteration(gdp, gamma, epsilon)
    #     # If value_iteration has not been implemented the return value is None.
    #     self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
    #     # It needs to return a dictionary.
    #     self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
    #     # Correct values
    #     v_correct = {(4, 0): 0.10266189300000003,
    #                  (3, 4): 0.30706773743750004,
    #                  (4, 3): 1.0301671918125004,
    #                  (3, 1): 0.4345592223750001,
    #                  (4, 6): 0.08374417700000003,
    #                  (0, 2): 0.48612293173437504,
    #                  (0, 5): 0.19358961775000008,
    #                  (2, 2): 2.49977098040625,
    #                  (1, 0): 0.18268291700000006,
    #                  (1, 6): 0.07801445600000002,
    #                  (2, 5): 0.031878611000000015,
    #                  (1, 3): 2.4634987229218748,
    #                  (4, 2): 0.48612293173437515,
    #                  (3, 0): 0.18268291700000006,
    #                  (4, 5): 0.19358961775000003,
    #                  (3, 3): 2.4634987229218748,
    #                  (3, 6): 0.07801445600000002,
    #                  (0, 1): 0.2255469297500001,
    #                  (2, 4): 2.4272264654374998,
    #                  (1, 2): 1.0327542465625004,
    #                  (0, 4): 0.44794267150000006,
    #                  (2, 1): 0.24141941575000025,
    #                  (1, 5): 0.13231929375,
    #                  (3, 2): 1.0327542465625004,
    #                  (4, 1): 0.22554692975000004,
    #                  (3, 5): 0.13231929375000004,
    #                  (4, 4): 0.44794267150000017,
    #                  (0, 0): 0.10266189300000002,
    #                  (1, 1): 0.43455922237500016,
    #                  (0, 3): 1.0301671918125004,
    #                  (2, 0): 0.11294878000000011,
    #                  (1, 4): 0.3070677374375001,
    #                  (0, 6): 0.08374417700000002,
    #                  (2, 3): 1.99609375,
    #                  (2, 6): 0.05105955400000002}
       
    #     for s in v:
    #         self.assertAlmostEqual(v[s],v_correct[s],
    #                                msg="Values differ for GridMDP example 3. Check value_iteration and value_of", places = 6)
            
                          
        
# class TestValueIterationsTSM(unittest.TestCase):
#     """
#     Tests using the TwoStateMachine
#     NOTE: IF these fail, check that test_twostatemachine.py passes all tests first.
#     """
#     def setUp(self):
#         self.tsm = TwoStateMachine()

#     def test_TSM_value_of(self):
#         """
#         This function uses TwoStateMachine to test different aspects
#         of valueiteration.py 
#         Note: Assumes a correct implementation of TwoStateMachine.
#         """
#         gamma = 0.5
#         # Call one step of value_of using some dummy values
#         x = value_of(self.tsm, TwoStateMachine.States.upright,
#                      TwoStateMachine.Actions.walk,
#                      {TwoStateMachine.States.upright : 0,
#                       TwoStateMachine.States.prone : 0},
#                      gamma)

#         # If value_of is not implemented it will return None
#         self.assertIsNotNone(x, msg = "Check TASKs 1.x and 2.1.")
#         # Compare with correct value.
#         self.assertAlmostEqual(x, 18.0, places = 4,
#                                msg = "Check TASKs 1.x and 2.1.")
        
#     def test_TSM_valueiteration(self):
#         """
#         This function uses TwoStateMachine to test different aspects
#         of valueiteration.py 
#         Note: Assumes a correct implementation of TwoStateMachine.
#         """
#         gamma = 0.5
#         epsilon = 0.01
#         # Call value_iteration
#         vi = value_iteration(self.tsm, gamma, epsilon)
#         # If value_iteration has not been implemented the return value is None.
#         self.assertIsNotNone(vi, msg = "Check TASKS 1.x and 2.2.")
#         # It needs to return a dictionary.
#         self.assertIsInstance(vi, dict, msg = "Check TASKs 1.x and 2.2")

#         # Compute the analytic solution and compare values.
#         va = self.tsm.analytic(gamma)
        
#         # Analytic and value iteration algorithm close enough?
#         self.assertAlmostEqual(vi[TwoStateMachine.States.upright],
#                                va[TwoStateMachine.States.upright],
#                                places=2,
#                                msg = "TwoStateMachine value_iteration and analytic differs substantially.")
#         self.assertAlmostEqual(vi[TwoStateMachine.States.prone],
#                                va[TwoStateMachine.States.prone],
#                                places=2,
#                                msg = "TwoStateMachine value_iteration and analytic differs substantially.")
        
#         # Make and test policy. Doesn't make much sense for
#         # the TSM as it only has one action. 
#         pi = make_policy(self.tsm, vi, gamma)
#         # Policy when standing is to walk
#         self.assertEqual(pi[TwoStateMachine.States.upright],
#         TwoStateMachine.Actions.walk,
#                          msg = "Wrong policy for TwoStateMachine.")
#         # Policy when prone is to stand
#         self.assertEqual(pi[TwoStateMachine.States.prone],
#                          TwoStateMachine.Actions.stand,
#                          msg = "Wrong policy for TwoStateMachine.")


            

if __name__ == "__main__":
    unittest.main()
