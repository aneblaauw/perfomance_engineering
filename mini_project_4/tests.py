import unittest


from models import Calculator, createFromBenchmark, swapPositions, createFromUncertainBenchmark
from utils import *

import numpy as np

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_1.txt'
        self.problem = createFromBenchmark(filename)

        #filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_3.txt'
        #self.problem_uncertain = createFromUncertainBenchmark(filename)
    

    def test_swap(self):
        schedule = [(1, 0), (2, 0), (1, 1), (3, 0), (1, 2), (2, 1), (3, 1), (3, 2)]
        new_scedule = swapPositions(schedule, 0, 1)
        self.assertEqual(new_scedule, [(2, 0), (1, 0), (1, 1), (3, 0), (1, 2), (2, 1), (3, 1), (3, 2)])
    
    def test_schedules(self):
        # Testing creating different schedules

        mixed_schedule = createMixedSchedule(self.problem)
        self.assertEqual(mixed_schedule,[(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (1, 2), (3, 1), (3, 2)])

        backwards_schedule = createBackwardsSchedule(self.problem)
        self.assertEqual(backwards_schedule, [(3, 0), (3, 1), (3, 2), (2, 0), (2, 1), (1, 0), (1, 1), (1, 2)])
    
    def test_translate_to_predict(self):
        schedule = [(1, 0), (2, 0), (1, 1), (3, 0), (1, 2), (2, 1), (3, 1), (3, 2)]
        y = translate_to_predict(schedule)
        print(y)
    
    def test_getRandomSchedules(self):
        all_schedules = getAllSchedules(self.problem)

        schedules = getRandomSchedules(all_schedules, 3)
        self.assertEqual(3, len(schedules))
        for i in range(3):
            self.assertEqual(True, possibleSchedule(schedules[i], self.problem))

    
    
if __name__ == '__main__':
    unittest.main()
