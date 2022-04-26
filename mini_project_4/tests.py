from fileinput import filename
import unittest


from models import Problem, Calculator





class Test(unittest.TestCase):
    def setUp(self):
        filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_1.txt'
        self.problem = Problem()
        
        self.problem.createFromBenchmark(filename)
    
    def test_Schedule(self):
        print('Problem oversikt')
        print(self.problem)
        print('Schedule:')
        print(self.problem.getSchedule())
    
    def test_calculator(self):
        calc = Calculator()

        filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_1.txt'
        problem = Problem()
        
        problem.createFromBenchmark(filename)
        time = calc.totalOperationTime(problem)
        print(time)

    
    


if __name__ == '__main__':
    unittest.main()