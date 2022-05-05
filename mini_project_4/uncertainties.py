
from models import createFromUncertainBenchmark, Calculator

filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_3.txt'
problem = createFromUncertainBenchmark(filename)

# just to see that it works
print('Problem:')
print(problem)
print('Schedule: ')
print(problem.getSchedule())

# TODO: printe, avg, min, og max value
print(problem.printProblem(True))


# find the average cost of a schedule
calc = Calculator()
print('Average makespan for the schedule: ', problem.getSchedule())
print(calc.averageOperationTime(problem.getSchedule(), problem))
