from itertools import permutations
import random
from utils import createSimpleSchedule, possibleSchedule, swapPositions, createBackwardsSchedule, createMixedSchedule, translate_to_predict, getRandomSchedules, getAllSchedules
from math import inf

class Calculator:

    def __init__(self) -> None:
        pass

    def totalOperationTime(self, problem, schedule, case='AVERAGE'):
        # criterias:
        #   1: the same machine can only do one job at a time
        #   2: the jobs must be completed in the given order

        # create one list for every machine
        # reset the operations list for the machines
        for machine in problem.machines:
            machine.operations=[]


        for job_id, operation in schedule:
            job = problem.getJob(job_id)
            operation = job.operations[operation]
            # can the job start? -> does any of the machines contain the job_id
            # find earliest start for given machine for the operation
            earliest_start = len(operation.machine.operations)
    
            for machine in problem.machines:
                start, stop = machine.getLastJob(job_id)

                if stop == earliest_start:
                    # does not need to consider the order of the jobs with this id
                    if stop > 0:
                        earliest_start = stop +1
                elif stop > earliest_start:
                    # must wait for machine to finish the job
                    earliest_start = stop +1 

            # Add operation to machine
            operation.machine.addOperation(operation, job_id, earliest_start, case=case)
        # add deadtime to the machines so everyone "finishes at the same time"
        total_time = 0
        for machine in problem.machines:
            if total_time < len(machine.operations):
                total_time = len(machine.operations)
        
        for machine in problem.machines:
            machine.addDeadTime(total_time - len(machine.operations))

        return total_time


    def allCandidateSchedules(self, problem):
        """
        Generate the list all candidate schedules.
        Calculate the makespan of a problem.
        """
        
        """
        Goes through the problem and finds every possible schedule
        [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]
        The important thing is that (1, 0) comes before (1,1) and so on
        """
        
        # First create the straight forward schedule
        # iterates through the jobs and returns a schedule of the different jobs
        schedule = createSimpleSchedule(problem)

        
        all_schedules = list(permutations(schedule))
        print('Length before removing: ', len(all_schedules))
        possible_schedules = []
        for i in range(len(all_schedules)):
            s = all_schedules[i]
            possible = possibleSchedule(s, problem)
            if possible:
                possible_schedules.append(list(s))
        
        print('Length after removing: ', len(possible_schedules))
        return possible_schedules
    
    def gradientDescendant(self, problem, set_size = 3000, all_schedules = None):
        # Step 1: create a random schedule
        
        # First find a random schedule
        if all_schedules == None:
            # create new all schedules
            all_schedules = getAllSchedules(problem, set_size)

        schedule = getRandomSchedules(all_schedules, 1)[0]
        
        # Step 2: find the nearest neighbours to this schedule that works, and find the best solution among them
        makespan = self.totalOperationTime(problem, schedule)
        better_option = schedule
        optimal = False

        count = 0
        while not optimal:
            
            optimal = True # assumes this solution is optimal
          
            for i in range(1, len(schedule)):
                neighbour = swapPositions(schedule, i-1, i)
       
                # check if this option has already been calculated
                count += 1
                # check if this schedule is possible
                if possibleSchedule(neighbour, problem):
                    if self.totalOperationTime(problem, neighbour) < makespan:
                        # Then this is the better option
                        better_option = neighbour
                        makespan = self.totalOperationTime(problem, better_option)
                        optimal = False # the last solution was not optimaler_option, makespan, count

    def gradientDescendant2(self, problem, set_size= 3000, all_schedules=None):
        # Step 1
        # create a random schedule
        
        # First create the straight forward schedule
        # iterates through the jobs and returns a schedule of the different jobs
        if all_schedules == None:
            # create new all schedules
            all_schedules = getAllSchedules(problem, set_size)

        random_start = getRandomSchedules(all_schedules, 3)
        schedule1 = random_start[0]
        schedule2 = random_start[1]
        schedule3 = random_start[2]
        
        
        archive = [schedule1, schedule2, schedule3] # an archive for storing already checked options

        results = {'1': [], '2': [], '3': []}

        # Step 2
        # Schedule 1
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbour(schedule1, archive, problem, self)
        results['1'] = [best_option, makespan, count]
        
        # Step 3
        #  Repeat for Schedule 2
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbour(schedule2, archive, problem, self)
        results['2'] = [best_option, makespan, count]

        # Step 4
        #  Repeat for Schedule 3
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbour(schedule3, archive, problem, self)
        results['3'] = [best_option, makespan, count]
        
        # find the best result
        best = None
        best_makespan = inf
        total_count = 0
        for key, value in results.items():
            total_count += value[2]
            if value[1] < best_makespan:
                best = value[0]
                best_makespan = value[1]
        
        

        return best, best_makespan, total_count
    
    def gradientDescendant3(self, problem, regression_model,set_size= 3000, all_schedules=None):
        # Step 1
        # create a random schedule
        
        # First create the straight forward schedule
        # iterates through the jobs and returns a schedule of the different jobs
        if all_schedules == None:
            # create new all schedules
            all_schedules = getAllSchedules(problem, set_size)

        random_start = getRandomSchedules(all_schedules, 3)
        schedule1 = random_start[0]
        schedule2 = random_start[1]
        schedule3 = random_start[2]
        
        
        
        archive = [schedule1, schedule2, schedule3] # an archive for storing already checked options

        results = {'1': [], '2': [], '3': []}

        # Step 2
        # Schedule 1
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbourML(schedule1, archive, problem, self, regression_model)
        results['1'] = [best_option, makespan, count]
        
        # Step 3
        #  Repeat for Schedule 2
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbourML(schedule2, archive, problem, self, regression_model)
        results['2'] = [best_option, makespan, count]

        # Step 4
        #  Repeat for Schedule 3
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        best_option, makespan, count = nearestNeighbourML(schedule3, archive, problem, self, regression_model)
        results['3'] = [best_option, makespan, count]
        
        # find the best result
        best = None
        best_makespan = inf
        total_count = 0
        for key, value in results.items():
            total_count += value[2]
            if value[1] < best_makespan:
                best = value[0]
                best_makespan = value[1]
        
        return best, best_makespan, total_count
    
    def averageOperationTime(self, schedule, problem):
        """A stochastic simulation method to calculate 
        mean value of total processing time of a schedule."""
        
        # to calculate the average, we will simply calculate the operation time for all three cases and find the average
        max = self.totalOperationTime(problem, schedule, case='WORST')
        avg = self.totalOperationTime(problem, schedule, case='AVERAGE')
        min = self.totalOperationTime(problem, schedule, case='BEST')

        print('Min: ', min)
        print('Avg: ', avg)
        print('Max: ', max)


        return (min + avg + max) / 3

    
def nearestNeighbour(schedule, archive, problem, calculator):

    makespan = calculator.totalOperationTime(problem, schedule)
    better_option = schedule
    optimal = False
    count = 0
    while not optimal:
        
        optimal = True # assumes this solution is optimal
        for i in range(1, len(schedule)):
            neighbour = swapPositions(schedule, i-1, i)
            # check if this option has already been calculated
            if neighbour not in archive:
                count += 1
                archive.append(neighbour)
                # check if this schedule is possible
                if possibleSchedule(neighbour, problem):
                    if calculator.totalOperationTime(problem, neighbour) < makespan:
                        # Then this is the better option
                        better_option = neighbour
                        makespan = calculator.totalOperationTime(problem, better_option)
                        optimal = False # the last solution was not optimal
        
        schedule = better_option
    
    return better_option, makespan, count

def nearestNeighbourML(schedule, archive, problem, calculator, regression_model):

    makespan = calculator.totalOperationTime(problem, schedule)
    better_option = schedule
    optimal = False
    count = 0
    while not optimal:
        
        optimal = True # assumes this solution is optimal
        for i in range(1, len(schedule)):
            neighbour = swapPositions(schedule, i-1, i)
            # check if this option has already been calculated
            if neighbour not in archive:
                count += 1
                archive.append(neighbour)
                # check if this schedule is possible
                if possibleSchedule(neighbour, problem):
                    #guess the result time for the noighbour
                    prediction= regression_model.predict([translate_to_predict(schedule)])
                    if prediction <= makespan:
                        # if the guess is not better than the solution found -> add to archive and don't calculate
                        if calculator.totalOperationTime(problem, neighbour) < makespan:
                            # Then this is the better option
                            better_option = neighbour
                            makespan = calculator.totalOperationTime(problem, better_option)
                            optimal = False # the last solution was not optimal
        
        schedule = better_option
    
    return better_option, makespan, count

    


        