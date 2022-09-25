from network import *
from cpt import *
from data.mapping import * 
import numpy as np
import re
import unittest

def is_answer_close(a, b, EPSILON = 1e-2):
    return abs(a - b) <= EPSILON


class TestCPT(unittest.TestCase):
    """
    Test implementation of CPT and sampling.
    """

   
    def setUp(self):
        # Load data
        filename = "data/hs.txt"
        self.data = np.loadtxt(filename, delimiter=" ")
        # Construct same bayesian network
        network = Network(self.data)
        # You need to list the nodes so that parents are introduced before children
        # You can inspect data.mapping to see all the features
        network.append_node(MEDICALSERV, "MEDICALSERV", [])
        network.append_node(SCHOOLHYMN, "SCHOOLHYMN", [MEDICALSERV])
        network.append_node(MILSERVICE, "MILSERVICE", [MEDICALSERV])
        network.append_node(METROPOLIS, "METROPOLIS", [SCHOOLHYMN])
        network.append_node(NATO, "NATO", [MILSERVICE])
        network.append_node(SAIMAASEAL, "SAIMAASEAL", [SCHOOLHYMN, MILSERVICE])
        self.network = network

   
    # def test_1_conditional_probability(self):
    #     """
    #     Check `get_conditional_probability`.
    #     """
    #     tests = [({SAIMAASEAL : 1}, {MILSERVICE : 1, SCHOOLHYMN: 1}, ["SAIMAASEAL", "MILSERVICE", "SCHOOLHYMN"], 0.857),
    #         ({NATO : 1}, {MILSERVICE : 0}, ["NATO", "-MILSERVICE"], 0.82),
    #         ({MEDICALSERV : 1}, {}, ["MEDICALSERV"], 0.128),
    #         ({SAIMAASEAL : 1}, {MILSERVICE : 0, SCHOOLHYMN: 1}, ["SAIMAASEAL", "-MILSERVICE", "SCHOOLHYMN"], 0.790)]

    #     for query, conditions, fields, answer in tests:
    #         prob = get_conditional_probability(self.data, query, conditions)
    #         self.assertTrue(is_answer_close(prob, answer), "Conditional probability failed: got {}, true answer {}".format(prob, answer))

    # def test_2_cpt(self):
    #     """
    #     Check `construct_probability_table`.
    #     """
    #     tests = [(SAIMAASEAL, [MILSERVICE, SCHOOLHYMN], ["SAIMAASEAL", "MILSERVICE", "SCHOOLHYMN"], {"0 0":0.587, "0 1":0.790, "1 0":0.834, "1 1":0.857}),]

    #     for query, conditions, fields, answer in tests:
    #         table = construct_probability_table(self.data, query, conditions)

    #         cptstr = "CPT for P({}|{})".format(fields[0], " & ".join(fields[1:]))
    #         for key, probability in table.items():
    #             assignments = re.findall(".([0-9]+):([0-1]).", key)
    #             str_assignment = " ".join([val for _, val in assignments])
    #             out_str_assignment = " ".join(f"{k} = {v}" for (k,v) in zip(fields[1:],assignments[:-1]))
    #             self.assertTrue(is_answer_close(answer[str_assignment], probability),
    #                             f"{cptstr} contains an error for assignment {out_str_assignment}. Correct probability: {probability}, result: {answer[str_assignment]}.")

    def test_3_brute_force(self):
        """
        Check `brute_force`.
        """
        tests = [([MILSERVICE], ([MEDICALSERV, SAIMAASEAL, METROPOLIS], [0, 0, 0]), ["MILSERVICE", "MEDICALSERV", "SAIMAASEAL", "METROPOLIS"], 0.183)]

        for query, (E,e), fields, answer in tests:
            prob = brute_force(self.network, query, E, e)

            estr = "Calculating P({}|{})".format(fields[0], " & ".join(fields[1:]))
            self.assertTrue(is_answer_close(answer, prob),
                           "Error {}; True answer: {} while yours: {}".format(estr,answer, round(prob, 3)))

    # def test_4_sampling(self):
    #     """
    #     Check `approximate_distribution`.
    #     """
    #     tests = [([MILSERVICE], ([MEDICALSERV, SAIMAASEAL, METROPOLIS],  [0, 0, 0]), ["MILSERVICE", "MEDICALSERV", "SAIMAASEAL", "METROPOLIS"], 0.183)]

    #     for query, (E,e), fields, answer in tests:
    #         prob = [approximate_distribution(self.network, query, E, e) for _ in range(3)]
    #         estr = "Calculating P({}|{})".format(fields[0], " & ".join(fields[1:]))
    #         self.assertTrue(any([is_answer_close(answer, p, EPSILON = 3e-2) for p in prob]),
    #             "Error {}; True answer {} while yours: {}".format(estr,answer, round(np.average(prob), 3)))


if __name__ == "__main__":  
    unittest.main()
