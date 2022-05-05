
'''
Create classes for machines, jobs, operations and problems. Define Get and Set
methods to access their fields.
Hint: Problems should be managed according to the factory patterns, i.e. it should
be possible to create machines, jobs and operations via methods of the class Problem.
'''

from itertools import permutations

class Problem:
    '''
    Consists of many machines and jobs
    '''

    def __init__(self, machines = [], jobs = []) -> None:
        self.machines = machines # trengs denne
        self.jobs = jobs
    
    def __str__(self) -> str:
        '''
        job 1 = [(0, 3), (1, 2), (2, 2)]
        job 2 = [(0, 2), (2, 1), (1, 4)]
        job 3 = [(1, 4), (2, 3)]
        '''
        s = ''
        for job in self.jobs:
            s += '%s = %s' % (job, job.printOperations())
            s += ' /n '
        
        return s
    
    def printMachines(self):
        s = '['
        for machine in self.machines:
            s += '%s, ' % machine
        
        s += ']'
        return s
    
    def printJobs(self):
        s = '['
        for job in self.jobs:
            s += '%s, ' % job
        
        s += ']'
        return s
    
        
    def getMachine(self, id):
        for machine in self.machines:
            if machine.id == id:
                return machine
        raise Exception("Machine does not exist.")
            
    def getJob(self, id):
        for job in self.jobs:
            if job.id == id:
                return job
        raise Exception("Job does not exist.")
    
    def getJobs(self):
        jobs = []
        for job in self.jobs:
            jobs.append(job.id)
        
        return jobs

    
    def getSchedule(self):
        '''
        The operations in the schedule is on the format (job_id, job_nr) -> 
        job_nr is the index of the operation in the job.operations list'''
        # iterates through the jobs and returns a schedule of the different jobs
        schedule = []
        for job in self.jobs:
            for i in range(len(job.operations)):
        
                schedule.append((job.id, i))
        print(schedule)
        return schedule
    
    def addOperationToMachine(self, operation, job_id):
        # adds the operation to the given machine but must also add deadtime to the other machines
        for machine in self.machines:
            if machine == operation.machine:
                machine.addOperation(operation, job_id)
            else:
                machine.addDeadTime(operation.time)




class Calculator:
    """Task 7.
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

        job_ids = problem.getJobs()
        
        # First create the straight forward schedule
        # iterates through the jobs and returns a schedule of the different jobs
        schedule = []
        for job in problem.jobs:
            for i in range(len(job.operations)):
                schedule.append((job.id, i))

        
        all_schedules = list(permutations(schedule))
        print('Length before removing: ', len(all_schedules))
        possible_schedules = []
        for i in range(len(all_schedules)):
            s = all_schedules[i]
            job_count = {id:-1 for id in job_ids}
            possible = True
            for job in s:
                job_id = job[0]
                nr = job[1]
                if nr > job_count[job_id]:
                    job_count[job_id] = nr
                else:
                    possible = False
                    break
            if possible:
                possible_schedules.append(list(s))
        
        print('Length after removing: ', len(possible_schedules))
        '''
        for schedule in possible_schedules:
            print(schedule)
        '''
        










class Machine:
    '''
    A machine is needed to do a job
    Must have an unique id
    Must have a sequence of jobs?
    '''
    def __init__(self, id) -> None:
        self.id = id
        self.operations = [] # the array with jobs for a set machine, when jobs are added, it will look like [(operation),(operation),,,,]
        # Every element last 1 time unit

    def __str__(self) -> str:
        return 'Machine %s' % self.id
    

    '''
    @property
    def operations(self):
        return self.operations
    '''
    def getLastJob(self, job_id):
        # find the start index and end index of the last job with this id the machine performed
        # return on format start, stop or 0,0 if it doesn't exist
        start = 0
        stop = 0
        for i in range(len(self.operations)):
            if self.operations[i] == job_id:
                start = i
                break
        
        for i in range(len(self.operations) -1, -1, -1):
            if self.operations[i] == job_id:
                stop = i
                break
        
        return start, stop
        


    def addOperation(self, operation, job_id, start):
        # adds an operation to a machine

        # if start is later than current length of operations -> add deadtime to the machine
        if start > len(self.operations):
            self.addDeadTime(start - len(self.operations))

        for i in range(operation.timespan):
            self.operations.append(job_id)
    
    def addDeadTime(self, timespan):
        for i in range(timespan):
            self.operations.append(0)


class Job:
    '''
    A job consists of an array of operations
    Each job must have a unique id
    
    job 0 = [(0, 3), (1, 2), (2, 2)]
    job 1 = [(0, 2), (2, 1), (1, 4)]
    job 2 = [(1, 4), (2, 3)]
    '''
    def __init__(self, id) -> None:
        self.id = id
        self.operations = [] # sequence of operations [(0, 3), (1, 2), (2, 2)]
    
    def __str__(self) -> str:
        return 'Job %s' % self.id
    
    def printOperations(self):
        op = '['
        for operation in self.operations:
            s = '(%s,%s)' % (operation.machine.id, operation.timespan)
            op += s
            op += ', '
        op += ']'
        return op

    def addOperation(self, operation):
        self.operations.append(operation)
    

class Operation:
    '''
    An operation is a combination of a machine and a timespan
    (0, 3) -> Machine 0, timespan 3
    Belongs to a job
    '''
    
    def __init__(self, machine, timespan) -> None:
        self.machine = machine
        self.timespan = timespan

    def __str__(self) -> str:
        return '(%s,%s)' % (self.machine.id, self.timespan)



class Printer:
    """Task 5.
    Venter litt med denne, til vi vet hva vi vil printe.

    Design a printer for problems (and results), with methods to export problems into
    files.
    """
    def __init__(self) -> None:
        pass