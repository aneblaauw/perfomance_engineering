
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