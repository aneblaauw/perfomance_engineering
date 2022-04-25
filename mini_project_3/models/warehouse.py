# Handles the operations in the warehouse

from .cell import *
from .truck import *
from .robot import *

class Warehouse:
    def __init__(self, catalog, floor_map = []) -> None:
        self.floor_map = floor_map # an double linked array of cells, where cells are placed according to coordinates
        self.catalog = catalog
        self.robots = [] # array of robots,maybe not needed in initializing
        self.client_orders = [] # client orders is added along the way
        self.deliveries = [] # deliveries are added along the way
        self.deliveryTruck = Truck()
    
    def jobToBeDone(self):
        # returns true if there is something that needs to be done in the warehouse,false if not
        if len(self.client_orders) > 0:
            return True
        if len(self.deliveries) >0:
            return True
        for robot in self.robots:
            if not robot.available():
                return True
        
        return False
    
    def addProductToTruck(self, product):
        

        if self.deliveryTruck.canAdd(product):
            self.deliveryTruck.add_product(product, 1)

        
        else:
            print('Truck is full, drives away')
            # truck drives away and a new is created
            self.deliveryTruck = Truck()
            print('New truck is created')


    
    def addRobots(self, n =1):
        '''
        creates a given number of robots and adds it to the list'''
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
        
        alley = findAlley(storage_cell.x)

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
        # for testing purposes, return the route
        return route


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
        print('Delivery added')
        for robot in self.robots:
            if robot.available():
                self.addUnloadToRobot(robot, delivery)
    
    def addUnloadToRobot(self, robot, delivery):
        '''
        Adds a delivery to a robot and calculates the route it must go
        Takes the product from a truck and puts it in a storage cell
        '''
        # Step 1, find the  cell where the product can be placed
        print(delivery)
        product = list(delivery.products.keys())[0]
        for row in self.floor_map:
            for cell in row:
                if cell.type == Cell.STORAGE:
                    # TODO: check if the cell has room for the product
                    if cell.canAddProduct(product):
                        print('Cell to store product %s: ' % (product.sn))
                        print(cell.printCellInfo())
                        self.calculateRoute(cell, robot)
                        delivery.removeProduct(product, 1)
                        if len(delivery.products) == 0:
                            # delivery is finished unloading
                            self.deliveries.remove(delivery)
                            print('Delivery finished')
                        robot.products.append(product)
                        robot.action = Robot.UNLOAD
                        print('Delivery after added to robot: ', delivery)
                        return True
        return False
    
    def addClientOrder(self, client_order):
        self.client_orders.append(client_order)
        for robot in self.robots:
            if robot.available():
                self.addLoadToRobot(robot, client_order)
    
    def addLoadToRobot(self, robot, client_order):
        '''
        Adds a client_order to a robot and calculates the route it must go
        Takes the product from a truck and puts it in a storage cell
        '''
        # Step 1, find the  cell where the product can be placed
        print(client_order)
        product = list(client_order.orders.keys())[0]
        for row in self.floor_map:
            for cell in row:
                if cell.type == Cell.STORAGE:
                    # check if the cell contains wished product
                    if cell.containsProduct(product):
                        print('Cell to pickup product %s: ' % (product.sn))
                        print(cell.printCellInfo())
                        self.calculateRoute(cell, robot)
                        client_order.removeProduct(product, 1)
                        robot.product_to_pick_up = product
                        if len(client_order.orders) == 0:
                            # client_order is finished
                            self.client_orders.remove(client_order)
                            print('Client Order Finished')
                        robot.action = Robot.PICKUP
                        return True
        print('The product is not in the warehouse')
        client_order.removeProduct(product, 1)
        if len(client_order.orders) == 0:
                            # client_order is finished
                            self.client_orders.remove(client_order)
                            print('Client Order Finished')
        return False


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
        
        y = 1

        # the x_coordinate is depending on the size of the floor_map before the alley is added
        x = 1
        if len(self.floor_map) > 0:
            x = len(self.floor_map[0]) +1

        # Step 1: Create a numpy array for storing the new alley
        alley = []
        index = 0 # the index for the rows in the floor_map

        # Step 2, create the top ailse
        # coordinates for the first storage cell
        
        for i in range(6):
            # create the storage cells
            storage1 = Cell('S',x,y)
            unload1 = Cell('L', x + 1, y)
            move1 = Cell('M', x + 2, y, direction='UP')

            
            move2 = Cell('M', x + 3, y, direction='DOWN')
            unload2 = Cell('L', x + 4, y)
            storage2 = Cell('S',x + 5,y)

            #add the cells to the floor map
            createOrAppend(self.floor_map, [storage1, unload1, move1, move2,  unload2, storage2], index)
            index += 1
            y = y+1
        
        # Step 3: add the middle

        unload1 = Cell('L', x, y)
        unload2 = Cell('L', x +1, y)
        movetop1 = Cell('M', x+2, y,  direction='UP')
        movetop2 = Cell('M', x+3, y,  direction='DOWN')
        unload3 = Cell('L', x+4, y)
        unload4 = Cell('L', x +5, y)

        createOrAppend(self.floor_map, [unload1,unload2, movetop1, movetop2,  unload3, unload4],index)
        index += 1

        y += 1
        x_cop = x
        row =  []
        for i in range(6):
            mover = Cell('M', x_cop, y, direction='RIGHT')
            row.append(mover)
            x_cop +=  1
        
        createOrAppend(self.floor_map, row, index)
        index += 1

        y += 1
        x_cop = x
        row =  []
        for i in range(6):
            movel = Cell('M', x_cop, y , direction='LEFT')
            row.append(movel)
            x_cop += 1

        createOrAppend(self.floor_map, row, index)
        index += 1

        y += 1

        unloadbottom1 = Cell('L', x, y)
        unloadbottom2 = Cell('L', x+1, y)
        movebottom1 = Cell('M', x+2, y,  direction='DOWN')
        movebottom2 = Cell('M', x+3, y,  direction='UP')
        unloadbottom3 = Cell('L', x+4, y)
        unloadbottom4 = Cell('L', x +5, y)

        createOrAppend(self.floor_map,[unloadbottom1,unloadbottom2, movebottom1, movebottom2,  unloadbottom3, unloadbottom4], index)
        index += 1
        #alley.append([unloadbottom1,unloadbottom2, movebottom1, movebottom2,  unloadbottom3, unloadbottom4])

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

            createOrAppend(self.floor_map, [storage1, unload1, move1, move2,  unload2, storage2], index)
            index += 1

            #alley.append([storage1, unload1, move1, move2,  unload2, storage2])
                    
    
    def nextAction(self, robot):
        # location: (x,y)
        # route: double linked list
        # availability: boolean (true: pick-up, false: deliver)
        
        if robot.route is not None:
            print('Robot must follow route')
            # continue to the next step in the route and update the current location
            robot.currentLocation = robot.route.pop(0) # this takes 10 seconds

            # check if current location is the storage cell
            currentCell = Cell('L', 0, 8)
            if not robot.currentLocation in [[0,8], [0,9]]:
                currentCell = self.floor_map[robot.currentLocation[1]-1][robot.currentLocation[0]-1]

            if currentCell.type == Cell.STORAGE:
                if robot.action == Robot.PICKUP:
                    # remove product from shelf on cell and add to robot
                    robot.products.append(robot.product_to_pick_up)
                    currentCell.removeProductFromShelf(robot.product_to_pick_up)
                    robot.product_to_pick_up = None
                    
                elif robot.action == Robot.UNLOAD:
                    # add the product to the shelf on the cell and remove from robot
                    currentCell.addProductToShelf(robot.products.pop())
                    
            
            if len(robot.route) == 0:
                if robot.action == Robot.PICKUP:
                    while len(robot.products) > 0:
                        self.addProductToTruck(robot.products.pop())
                        print('product added to Truck')

                robot.route = None
                robot.currentLocation = [0,8]
                robot.action = Robot.WAITING
        
        else:
            print('Robot has no job, create a new one')
            # get a new job, either unload from truck or pick up from client order
            if len(self.deliveries) > 0:
                self.addUnloadToRobot(robot, self.deliveries[0])
            elif len(self.client_orders) > 0:
                self.addLoadToRobot(robot, self.client_orders[0])
    

def createOrAppend(floor_map, row, i):
    '''
    Help function for adding alleys
    Checks if the floor_map has the row, if so add the  new row to existing row, else create a newrow
    '''
    if i < len(floor_map):
        # add the cells to the row
        floor_map[i] += row
    else:
        # create new row with the cells
        floor_map.append(row)

def findAlley(x_coord):
    '''
    finds the alley the storage cell belongs to
    '''
    return -1 * (-x_coord // 6)