
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
        return schedule
    
    def addOperationToMachine(self, operation, job_id):
        # adds the operation to the given machine but must also add deadtime to the other machines
        for machine in self.machines:
            if machine == operation.machine:
                machine.addOperation(operation, job_id)
            else:
                machine.addDeadTime(operation.time)
