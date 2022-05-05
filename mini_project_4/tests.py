from fileinput import filename
import unittest

from utils import createFromBenchmark
from models import Problem, Calculator





class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_1.txt'
        self.problem = createFromBenchmark(filename)
           
    
    def test_Schedule(self):
        print('Problem:')
        print(self.problem)
        print('Schedule:')
        print(self.problem.getSchedule())
        self.assertEqual([(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)], self.problem.getSchedule())
    
    def test_calculator(self):
        calc = Calculator()
        time = calc.totalOperationTime(self.problem, self.problem.getSchedule())
        #time = 20
        for machine in self.problem.machines:
            s = 'Machine %s: %s' % (machine.id, machine.operations)
            print(s)
        self.assertEqual(15, time)
    
    def test_allSchedules(self):
        calc = Calculator()
        calc.allCandidateSchedules(self.problem)
    
    def test_makeSpan(self):
        schedule = [(1, 0), (2, 0), (1, 1), (3, 0), (1, 2), (2, 1), (3, 1), (3, 2)]
        calc = Calculator()
        time = calc.totalOperationTime(self.problem, schedule)
        self.assertEqual(13, time)

        for machine in self.problem.machines:
            s = 'Machine %s: %s' % (machine.id, machine.operations)
            print(s)

    
    


if __name__ == '__main__':
    unittest.main()