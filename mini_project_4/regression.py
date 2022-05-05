# in this experiment, we will test a quite large benchmark
# Experimenting with the gradient descendant function
from models import createFromBenchmark, Calculator

filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_2.txt'
problem = createFromBenchmark(filename)
print('Problem:')
print(problem)

calc = Calculator()
calc.gradientDescendant(problem)