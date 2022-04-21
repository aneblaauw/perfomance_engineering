class Printer:
    """Task3. In charge of printing all info related to the warehouse
    and its operation.
    """
    
    def __init__(self, warehouse) -> None:
        self.warehouse = warehouse

    def printFloorMap(self, ):
        s = '\nFloor Map\n'
        robot_loc = []
        for robot in self.warehouse.robots:
            robot_loc.append(robot.currentLocation)
        for i in range(len(self.warehouse.floor_map)): 
            if i == 7 or i == 8:
                if [0,i+1] in robot_loc:
                    s+= 'o'
                    
                else:
                    s+= ' '
            else:
                s+= '|'
            for cell in self.warehouse.floor_map[i]:
                if [cell.x, cell.y]  in robot_loc:
                    s += ' [ o ] '
                else:
                    s += ' %s ' % cell.printCellType()
            s += '| %s \n' % str(i +1)
        
        columns = len(self.warehouse.floor_map[0])
        for i in range(columns):
            s += '    %s  ' % str(i +1)
        
        print(s)

    def printFloorMapCord(self):
        s = '\n'
        for i in range(len(self.warehouse.floor_map)): 
            s+= '|'
            for cell in self.warehouse.floor_map[i]:
                s += ' %s ' % cell.printCellCord()
            s += '| %s \n' % str(i +1)
        
        columns = len(self.warehouse.floor_map[0])
        for i in range(columns):
            s += '     %s   ' % str(i +1)
        
        print(s)
    
    def printCatalog(self):
        print(self.warehouse.catalog)