from models import Cell
from  robot import Robot

class Warehouse:
    def __init__(self, floor_map, catalog) -> None:
        self.floor_map = floor_map # an double linked array of cells, where cells are placed according to coordinates
        self.catalog = catalog
        self.robots = [] # array of robots,maybe not needed in initializing
        self.client_orders = [] # client orders is added along the way
        self.deliveries = [] # deliveries are added along the way
    
    def addRobots(self, n =1):
        '''
        creates a given numberof robots and adds it to the list'''
        for i in range(n):
            self.robots.append(Robot())
    
    def calculateRoute(self, storage_cell, robot):
        '''
        Calculates the route for a robot from start(0,8) to the wished storage cell and 
        back to cell (0,9)
        '''


        route = [robot.currentLocation]

        # TODO: check if the storage cell lies higher or lower than start
        if storage_cell.y < 8:
            direction = 'UP'
        else:
            direction = 'DOWN'
        
        # TODO: check if the storage cell lies on the left or right  side of the aisle
        # find a way tocalculate the number for the alley, and check if the coordinate lies left or right for themiddle of that  ails
        # until then
        alley = 1 # must use the floor map to find the alley

        middle = 3 + 6 * (alley-1)
        if storage_cell.x > middle:
            side = 'LEFT'
        else:
            side ='RIGHT'


        while not [storage_cell.x, storage_cell.y] in route:
            # calculate next step
            # First, we find the available options

            # We know that the robot should change direction at the middle cell
            current_x = route[-1][0]
            current_y = route[-1][1]
            if  current_x == middle:
                if direction == 'UP':
                    if  current_y == storage_cell.y:
                        if side == 'LEFT':
                            # Move towards the cell
                            # add the down cell, the unload cell and the storage cell
                            route.append([current_x +1, current_y])
                            route.append([current_x +2, current_y])
                            route.append([current_x +3, current_y])

                            # append the steps back as well
                            route.append([current_x +2, current_y])
                            route.append([current_x +1, current_y])
                        else:
                            # Move towards the cell
                            # add the unload cell and the storage cell
                            route.append([current_x -1, current_y])
                            route.append([current_x -2, current_y])

                            # append the steps back as well
                            route.append([current_x -1, current_y])
                            route.append([current_x, current_y])
                            route.append([current_x +1, current_y])
                    else:
                        # Move upwards
                        route.append([current_x, current_y -1])
                else:
                    if  current_y == storage_cell.y:
                        if side == 'LEFT':
                            # Move towards the cell
                            # add the down cell, the unload cell and the storage cell
                            route.append([current_x +1, current_y])
                            route.append([current_x +2, current_y])
                            route.append([current_x +3, current_y])
                            
                            # append the steps back as well
                            route.append([current_x +2, current_y])
                            route.append([current_x +1, current_y])
                        else:
                            # Move towards the cell
                            # add the unload cell and the storage cell
                            route.append([current_x -1, current_y])
                            route.append([current_x -2, current_y])

                            # append the steps back as well
                            route.append([current_x -1, current_y])
                            route.append([current_x, current_y])
                            route.append([current_x +1, current_y])
                            finished = True
                    else:
                        # Move upwards
                        route.append([current_x, current_y +1])
            else:
                # Move forwards
                route.append([current_x +1, current_y])
            
        # create the route back to base

        while not [0,9] in route:
            # we  have to move up- or downwards until we reach row 9
            current_x = route[-1][0]
            current_y = route[-1][1]

            if current_y == 9:
                # go left
                route.append([current_x-1, current_y])
            else:
                # go up or down
                if direction == 'UP':
                    # go down
                    route.append([current_x, current_y +1])
                else:
                    # go up
                    route.append([current_x, current_y-1])

        

        robot.route = route



    def add_product(self, product):
        # Assume the product exist
        '''
        Adds the product from the warehouse's catalogue
        '''
        if not product in self.catalog:
           self.catalog.products.append(product)

    def remove_product(self, product):
        '''
        Remove the product from the warehouse's catalogue
        '''
        if product in self.catalog:
            self.catalog.products.remove(product)   

    def addDelivery(self, delivery):
        self.deliveries.append(delivery)
        for robot in self.robots:
            if robot.available():
                self.addUnloadToRobot(robot, delivery)

        # find an available robot and give it a task
    
    def addUnloadToRobot(self, robot, delivery):
        '''
        Adds a delivery to a robot and calculates the route it must go
        Takes the product from a truck and puts it in a storage cell
        '''
        # Step 1, find the  cell where the product can be placed
        product = delivery.products.keys()[0]
        for row in self.floor_map:
            for cell in row:
                if cell.type == Cell.STORAGE:
                    # TODO: check if the cell has room for the product
                    if cell.canAddProduct(product):
                        self.calculateRoute(cell, robot)
                        delivery.removeProduct(product, 1)
                        robot.products.append(product)
                        return True
        return False

        

    def addClientOrders(self, order):
        self.client_orders.append(order)

    def removeClientOrders(self, order):
        self.client_orders.remove(order)

    def addAlley(self):
        '''
        Test for creating warehouses
        Floor map has to be a 2D list


        y_coord = 1st index
        x_coor  = 2nd index
        '''
        # Test first for creating the first alley
        x = 1
        y = 1

        # Step 1: Create a numpy array for storing the new alley
        alley = []

        # Step 2, create the top ailse
        # TODO: find the coordinates for the middle and end of the warehouse

        # coordinates for the first storage cell
        
        for i in range(6):
            # create the storage cells
            storage1 = Cell('S',x,y)
            unload1 = Cell('L', x + 1, y)
            move1 = Cell('M', x + 2, y, direction='UP')

            
            move2 = Cell('M', x + 3, y, direction='DOWN')
            unload2 = Cell('L', x + 4, y)
            storage2 = Cell('S',x + 5,y)

            alley.append([storage1, unload1, move1, move2,  unload2, storage2])

            # TODO: add the cells to the floor map
            y = y+1
        
        # Step 3: add the middle

        unload1 = Cell('L', x, y)
        unload2 = Cell('L', x +1, y)
        movetop1 = Cell('M', x+2, y,  direction='UP')
        movetop2 = Cell('M', x+3, y,  direction='DOWN')
        unload3 = Cell('L', x+4, y)
        unload4 = Cell('L', x +5, y)

        alley.append([unload1,unload2, movetop1, movetop2,  unload3, unload4])

        y += 1
        x_cop = x
        row =  []
        for i in range(6):
            mover = Cell('M', x_cop, y, direction='RIGHT')
            row.append(mover)
            x_cop +=  1
        alley.append(row)

        y += 1
        x_cop = x
        row =  []
        for i in range(6):
            movel = Cell('M', x_cop, y , direction='LEFT')
            row.append(movel)
            x_cop += 1

        alley.append(row)

        y += 1

        unloadbottom1 = Cell('L', x, y)
        unloadbottom2 = Cell('L', x +1, y)
        movebottom1 = Cell('M', x+2, y,  direction='DOWN')
        movebottom2 = Cell('M', x+3, y,  direction='UP')
        unloadbottom3 = Cell('L', x+4, y)
        unloadbottom4 = Cell('L', x +5, y)

        alley.append([unloadbottom1,unloadbottom2, movebottom1, movebottom2,  unloadbottom3, unloadbottom4])

        # Step 4: add bottom
        
        for i in range(6):
            y += 1
            # create the storage cells
            storage1 = Cell('S',x,y)
            unload1 = Cell('L', x + 1, y)
            move1 = Cell('M', x + 2, y, direction='DOWN')

            
            move2 = Cell('M', x + 3, y, direction='UP')
            unload2 = Cell('L', x + 4, y)
            storage2 = Cell('S',x + 5,y)

            alley.append([storage1, unload1, move1, move2,  unload2, storage2])
            

        # TODO: find a way to actually add the alley to the floor map
        # for now return the new alley
        self.floor_map = alley
    
    def nextAction(self, robot):
        # location: (x,y)
        # route: double linked list
        # availability: boolean (true: pick-up, false: deliver)
        
        
        if robot.route is not None:
            # continue to the next step in the route and update the current location
            robot.currentLocation = robot.route.pop(0) # this takes 10 seconds

            # check if current location is the storage cell
            currentCell = self.floor_map[robot.cuurentLocation[0]][robot.currentLocation[1]]

            if currentCell.type == Cell.STORAGE:
                if robot.action == Robot.PICKUP:
                    # TODO remove product from shelf on cell and add to robot
                    pass
                elif robot.action == Robot.UNLOAD:
                    # TODOD add the product to the shelf on the cell and remove from robot
                    pass
                

            if len(robot.route) == 0:
                robot.route = None
                robot.currentLocation = [0,8]
    
    