
'''
Create classes for machines, jobs, operations and problems. Define Get and Set
methods to access their fields.
Hint: Problems should be managed according to the factory patterns, i.e. it should
be possible to create machines, jobs and operations via methods of the class Problem.
'''


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
            s += '/n'
        
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
    
    def createFromBenchmark(self, filename):
        '''
        reads from txt file and creates a problem
        '''
        # TODO: fix filename path with sys.path eller noe
        
        try:
            with open(filename) as file:
                # line 1 -> create needed jobs and machines
                lines = file.readlines()
                info = lines[0].split(' ')
                
                n_jobs = int(info[0])
                n_machines = int(info[1])
                for i in range(n_jobs):
                    job = Job(i+1)
                    self.jobs.append(job)

                for i in range(n_machines):
                    machine = Machine(i+1)
                    self.machines.append(machine)

                # line 2 -> end is operations
                for i in range(1, len(lines)):
                    job = self.getJob(i)
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

                        index1 = i*2 +1 # mavhine index
                        index2 =i*2 +2 # time index

                        machineid = int(info[index1])
                        timespan = int(info[index2])
                      
                        operation = Operation(self.getMachine(machineid), timespan)
                        # add operation to the job
                        job.addOperation(operation)
                file.close()
                
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        
    def getMachine(self, id):
        for machine in self.machines:
            if machine.id == id:
                return machine
        
        #raise Exception("Machine does not exist.")
    
    def getJob(self, id):
        for job in self.jobs:
            if job.id == id:
                return job
        #raise Exception("Job does not exist.")
    
    def getSchedule(self):
        # iterates through the jobs and returns a schedule of the different jobs
        schedule = []
        print(self.printJobs())
        for job in self.jobs:
            for i in range(len(job.operations)):
                
                schedule.append((job.id, i))
        return schedule



class Calculator:
    def __init__(self) -> None:
        pass

    def totalOperationTime(self, problem):
        """Task7. Calculate the total operation time of a schedule."""
        schedule = problem.getSchedule()
        time = 0

        for job_id, operation in schedule:
            job = problem.getJob(job_id)
            operation = job.operations[operation]
            time += operation.timespan
        return time


    def allCandidateSchedules(self):
        """
        Generate the list all candidate schedules.
        Calculate the makespan of a problem.
        """
        
        pass


class Machine:
    '''
    A machine is needed to do a job
    Must have an unique id
    Must have a sequence of jobs?
    '''
    def __init__(self, id) -> None:
        self.id = id
        self.operations = [] # the array with jobs for a set machine, when jobs are added, it will look like [(operation),(operation),,,,]

    def __str__(self) -> str:
        return 'Machine %s' % self.id
    

    '''
    @property
    def operations(self):
        return self.operations
    '''

    def addOperation(self, operation):
        # adds an operation to a machine
        pass


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



    