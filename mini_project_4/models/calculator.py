from utils import createSimpleSchedule, possibleSchedule

class Calculator:
    """
    """
    def __init__(self) -> None:
        pass

    def totalOperationTime(self, problem, schedule):
        """Task7. Calculate the total operation time of a schedule."""
        # TODO: check if some of the machines can run at the same timne
        time = 0
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
            # TODO: calculations 
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
            operation.machine.addOperation(operation, job_id, earliest_start)
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
        Task 8.
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
        '''
        for schedule in possible_schedules:
            print(schedule)
        '''
        return possible_schedules
    
    def gradientDescendant(self, problem):
        # Step 1
        # create a random schedule

        job_ids = problem.getJobs()
        
        # First create the straight forward schedule
        # TODO: create random?
        # iterates through the jobs and returns a schedule of the different jobs
        schedule = []
        for job in problem.jobs:
            for i in range(len(job.operations)):
                schedule.append((job.id, i))
        

        # Step 2
        # find the nearest neighbours to this schedule that works, and find the best solution among them
        

        # Step 3
        # Repeat step 2 with the best soloution found
        
        # Step 4
        # When to stop: If the makespan of the closest neighbours doesn't beat the best solution already found
        
        
