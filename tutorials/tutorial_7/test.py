#!/usr/bin/env python3
import sys, os, json, copy, unittest, doctest
import lab

sys.setrecursionlimit(100000)

class TestTalent(unittest.TestCase):
    def test_01(self):
        self.run_case(1)

    def test_02(self):
        self.run_case(2)

    def test_03(self):
        self.run_case(3)

    def test_04(self):
        self.run_case(4)

    def test_05(self):
        self.run_case(5)

    def test_06(self):
        self.run_case(6)

    def test_07(self):
        self.run_case(7)

    def test_08(self):
        self.run_case(8)

    def test_09(self):
        self.run_case(9)

    def run_case(self, case):
        with open("cases/"+str(case)+'.in', 'r') as f:
            input_data = json.loads(f.read())
        with open("cases/"+str(case)+'.out', 'r') as f:
            expect = json.loads(f.read().replace("\'", '"').replace("(", '[').replace(")", ']'))
        result = self.select_candidates(input_data)
        self.verify(result, input_data, expect)
                
    def select_candidates(self, input_data):
        num_candidates = input_data["num_candidates"]
        num_talents = input_data["num_talents"]
        candidate_to_talents = input_data["candidate_to_talents"]
        talent_to_candidates = input_data["talent_to_candidates"]
        matrix = input_data["matrix"] #only needed for ui
        r = lab.select_candidates(num_candidates, num_talents,
                                  candidate_to_talents, talent_to_candidates)
        return r

    def verify(self, result, input_data, expect):
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(expect), msg="result of incorrect length")
        c_to_t = input_data["candidate_to_talents"]
        self.assertEqual(talents_covered(result, c_to_t), talents_covered(expect, c_to_t), \
                         msg = "incorrect talents covered")

def talents_covered(candidates, candidate_to_talents):
    covered = set()
    for c in candidates:
        covered |= set(candidate_to_talents[c])
    return covered

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
