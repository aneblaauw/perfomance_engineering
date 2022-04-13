# Contains helping methods



from models import Catalog, Product, Truck, Delivery, Cell, Warehouse

import random
import string
import numpy as np



def createCatalog(n=15):
    '''
    Creates a cataloge with the given number of products, the products are created with a random code and weight
    '''
    products = []
    for _ in range(n):
        # sn: 3AQ AAAA 1234
        sn = '3AQ '
        chars = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
        num = ' ' + str(random.randint(1000,9999))
        weight = random.randint(2,40) # kg
        product = Product(sn + chars + num, weight)
        products.append(product)
    catalog = Catalog(products)

    return catalog

def createTruckLoading(deliveries, max_weight=20000):
    # total weight truck: 20 tonn -> 20 000 kg
    '''
    Loads a truck unitl capacity is reached, max weight is 20 tons -> 20 000 kg
    '''
    load = []
    total_weight = 0
    for delivery in deliveries:
        if total_weight + delivery.get_total_weight() < max_weight:
            load.append(delivery)
            total_weight += delivery.get_total_weight()
    
    truck = Truck(load)

    return truck

def createRandomDelivery(catalog):
    dict = {}
    for i in range(5):
        index = random.randint(0, len(catalog.products) -1)
        quantity = random.randint(1,5)
        product = catalog.products[index]
        dict[product] = quantity

    delivery = Delivery(dict)
    return delivery

def createWareHouse(alleys_n, alleys_size, number_of_products = 15):
    # creates a warehouse from high level parameters
    floor_map = []
    floor_map = addAlley(floor_map)
    catalog = createCatalog(number_of_products)
    # wait with the robots
    warehouse = Warehouse(floor_map,catalog, None)
    return warehouse

def addAlley(floor_map):
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
    return alley
    
def printFloorMap(floor_map):
    s = '\nFloor Map\n'
    for i in range(len(floor_map)): 
        s+= '|'
        for cell in floor_map[i]:
            s += ' %s ' % cell.printCellType()
        s += '| %s \n' % str(i +1)
    
    columns = len(floor_map[0])
    for i in range(columns):
        s += '    %s  ' % str(i +1)
    
    print(s)

def printFloorMapCord(floor_map):
    s = '\n'
    for i in range(len(floor_map)): 
        s+= '|'
        for cell in floor_map[i]:
            s += ' %s ' % cell.printCellCord()
        s += '| %s \n' % str(i +1)
    
    columns = len(floor_map[0])
    for i in range(columns):
        s += '    %s  ' % str(i +1)
    
    print(s)

def calculateRoute(storage_cell):
    '''
    Calculates the route for a robot fram start(0,8) to the wished storage cell and 
    back to cell (0,9)
    '''

    route = [[0,8]]
    finished = False

    # TODO: check if the storage cell lies higher or lower than start
    if storage_cell.y < 8:
        direction = 'UP'
    else:
        direction = 'DOWN'
    
    # TODO: check if the storage cell lies on the left or right  side of the aisle
    # find a way tocalculate the number for the alley, and check if the coordinate lies left or right for themiddle of that  ails
    # until then
    alley = 1

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

    

    return route
                

        




def nextAction(location, route, availabilty):
    # location: (x,y)
    # route: double linked list
    # availability: boolean (true: pick-up, false: deliver)
    
    # 
    # if location == delivery cell -> route to storage cell
    # if location == storage_cell -> unload
    # if location == 
    
    
    pass







