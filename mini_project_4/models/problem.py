import os
import sys
from models import Operation, Job, Machine

class Problem:
    '''
    Consists of many machines and jobs. 
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
    
    def printProblem(self, uncertainty=False):
        
        s = ''
        for job in self.jobs:
            s += '%s = %s' % (job, job.printOperations(uncertainty))
            s += ' /n '
        
        return s
    
    def printMachines(self):
        s = '['
        for machine in self.machines:
            s += '%s, ' % machine
        
        s += ']'
        return s
    
    def printSchedule(self,schedule, makespan):
        print('Schedule: ', schedule)
        for machine in self.machines:
            s = 'Machine %s: %s' % (machine.id, machine.operations)
            print(s)
        print('Total makespan: ', makespan)

    
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
        return schedule
    
    def addOperationToMachine(self, operation, job_id):
        for machine in self.machines:
            if machine == operation.machine:
                machine.addOperation(operation, job_id)
            else:
                machine.addDeadTime(operation.time)
    
    def saveToFile(self, filename):
        ''''
        creates a benchmark for a problem and saves to file
        3 (n_machines) 3 (n_jobs) 8 (total_operations)
        3 (total operations) 3 (machine_id) 4(timespan) 2 2 1 1
        2 1 3 3 3
        3 2 2 1 4 3 1
        '''
        path = os.getcwd() + '/mini_project_4/benchmarks/' + filename

        f = open(path, 'w')

        n_machines = len(self.machines)
        n_jobs = len(self.jobs)
        total_operations = 0
        for job in self.jobs:
            total_operations += len(job.operations)
        
        f.write('%s %s %s \n' % (n_machines, n_jobs, total_operations))

        for job in self.jobs:
            total_operations = len(job.operations)
            s = str(total_operations) + ' '
            for operation in job.operations:
                machine_id = operation.machine.id
                timespan = operation.timespan
                s += '%s %s ' % (machine_id, timespan)
            s += '\n'

            f.write(s)
        
        f.close()


def createFromBenchmark(filename):
        try:
            with open(filename) as file:
                # line 1 -> create needed jobs and machines
                problem = Problem()
                lines = file.readlines()
                info = lines[0].split(' ')
                
                n_jobs = int(info[0])
                n_machines = int(info[1])

                for i in range(n_jobs):
                    job = Job(i+1)
                    problem.jobs.append(job)

                for i in range(n_machines):
                    machine = Machine(i+1)
                    problem.machines.append(machine)
                

                # line 2 -> end is operations
                for i in range(1, len(lines)):
                    job = problem.getJob(i)
                    info = lines[i].split(' ')
                    """
                    We know that from a line ['3', '3', '4', '2', '2', '1', '1\n']

                    [total operations, machine, time, machine, time, ...]

                    """
                    total_op = int(info[0])
                    for i in range(total_op): # 0,1,2
                        # if i =0, index = 1 and 2
                        # if i=1, index = 3 and 4
                        # if i=2, index = 5 and 6
                        # if i=3, index = 7 and 8

                        index1 = i*2 +1 # machine index
                        index2 =i*2 +2 # time index

                        machineid = int(info[index1])
                        timespan = int(info[index2])
                      
                        operation = Operation(problem.getMachine(machineid), timespan)
                        # add operation to the job
                        job.addOperation(operation)
                file.close()
            return problem
                
        except FileNotFoundError as fnf_error:
            print(fnf_error)


def createFromUncertainBenchmark(filename):
        '''
        Reads from txt file and creates a problem
        '''
        try:
            with open(filename) as file:
                # line 1 -> create needed jobs and machines
                problem = Problem()
                lines = file.readlines()
                info = lines[0].split(' ')
                
                n_jobs = int(info[0])
                n_machines = int(info[1])
                for i in range(n_jobs):
                    job = Job(i+1)
                    problem.jobs.append(job)

                for i in range(n_machines):
                    machine = Machine(i+1)
                    problem.machines.append(machine)

                # line 2 -> end is operations
                for i in range(1, len(lines)):
                    job = problem.getJob(i)
                    info = lines[i].split(' ')
                    """
                    We know that from a line ['3', '3', '1', '4', '5', '2', '1', '2', '2', '1', '1', '6\n']

                    [total operations, machine, best, avg, worst, machine, best, avg, worst ...]

                    """
                    total_op = int(info[0])
                    for i in range(total_op): # 0,1,2
                        # if i =0, index = 1 2, 3 and 4
                        # if i=1, index = 5, 6, 7 and 8
                        # if i=2, index = 9, 10, 11 and 12
                        # if i=3, index = 13, 14, 15 and 16

                        index1 = i*4 +1 # machine index
                        index2 =i*4 +2 # best index
                        index3 = i*4 +3 # avg index
                        index4 = i*4 +4 # worst index

                        machineid = int(info[index1])
                        best = int(info[index2])
                        timespan = int(info[index3])
                        worst = int(info[index4])
                      
                        operation = Operation(problem.getMachine(machineid), timespan, best=best, worst=worst)
                        # add operation to the job
                        job.addOperation(operation)
                file.close()
            return problem
                
        except FileNotFoundError as fnf_error:
            print(fnf_error)
    
