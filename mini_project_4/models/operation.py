class Operation:
    '''
    An operation is a combination of a machine and a timespan
    (0, 3) -> Machine 0, timespan 3
    Belongs to a job
    '''
    
    def __init__(self, machine, timespan, best=None, worst=None) -> None:
        self.machine = machine
        self.timespan = timespan
        if best == None:
            self.best = timespan
        else:
            self.best = best
        if worst == None:
            self.worst = timespan
        else:
            self.worst = worst

    def __str__(self) -> str:
        return '(%s,%s)' % (self.machine.id, self.timespan)