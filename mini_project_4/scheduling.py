# Experimenting with simple scheduling

from cmath import inf
from models import createFromBenchmark, Calculator


#TODO: fix sys path
filename = '/Users/ane/Projects/Performance Engineering/mini_project_4/benchmark_1.txt'
problem = createFromBenchmark(filename)
print('Problem:')
print(problem)
print('Schedule: ')
print(problem.getSchedule())


calc = Calculator()
time = calc.totalOperationTime(problem, problem.getSchedule())
print('Total operation time for the simplest solution: ', time)
for machine in problem.machines:
    s = 'Machine %s: %s' % (machine.id, machine.operations)
    print(s)


#finding the best solution by checking all possible solutions
schedules = calc.allCandidateSchedules(problem)
makespan = inf
best = None

for schedule in schedules:
    time = calc.totalOperationTime(problem, schedule)
    if time < makespan:
        makespan = time
        best = schedule

print('Best solution found: ', best)
print('Total operation time for the best solution: ', makespan)
for machine in problem.machines:
    s = 'Machine %s: %s' % (machine.id, machine.operations)
    print(s)