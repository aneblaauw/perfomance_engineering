import unittest


from models import Calculator, createFromBenchmark, swapPositions, createFromUncertainBenchmark

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
        print(new_scedule)

    
    
if __name__ == '__main__':
    unittest.main()
