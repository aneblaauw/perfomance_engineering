class Optimizer:

    def __init__(self, warehouse) -> None:
        self.warehouse = warehouse
        self.total_time = 0
    
    def calculateTimeRobot(self, route):
        '''
        calculates the time the given route will take
        '''
        time = 0 #s
        for coord in route:
            cell = self.warehouse.floor_map[coord[1]-1][coord[0]-1]
            time += cell.getTime()

        self.total_time += time
        return time
   

    
