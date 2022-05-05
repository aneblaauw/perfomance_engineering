

from distutils.log import error


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
        


    def addOperation(self, operation, job_id, start, case='AVERAGE'):
        if case not in ['WORST', 'BEST', 'AVERAGE']:
            raise ValueError('%s is not a valid option for case' % case)
        # adds an operation to a machine

        # if start is later than current length of operations -> add deadtime to the machine
        if start > len(self.operations):
            self.addDeadTime(start - len(self.operations))

        if case == 'AVERAGE':
            time = operation.timespan
        elif case == 'BEST':
            time = operation.best
        else:
            time = operation.worst

        for i in range(time):
            self.operations.append(job_id)
    
    def addDeadTime(self, timespan):
        for i in range(timespan):
            self.operations.append(0)
    