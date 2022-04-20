# Contains the models of this program and their functionalities

'''Type of products and catalogs;
– Products;
– Deliveries;
– Robots;
– Cells (storage cells, route cells, loading/unloading cells);
– The warehouse itself;
– Client orders.
'''



from datetime import datetime
from tkinter import RIGHT
from numpy import product

"""Task 1. Data structures to manage entities involved in the simulation process.
"""
class Catalog:
    def __init__(self, products) -> None:
        self.products = products # Array
    
    def __str__(self) -> str:
        string = 'Catalog \n'
        for product in self.products:
            string += ' %s –– %s kg\n' % (product.sn, product.weight)
        
        return string
    

class Product:
    def __init__(self, sn, weight) -> None:
        self.sn = sn
        if 2 <= weight <= 40: # make sure weight is between 2 and 40 kg
            self.weight = weight
        else:
            pass # TODO: bedre else


class Delivery:
    def __init__(self, products) -> None:
        self.products = products # dictionary on format {product1: quantity, product2: quantity, ...}
        self.created_at = datetime.today()
    
    def __str__(self) -> str:
        string = 'Delivery \n created at: %s \n' % self.created_at
        
        for product, quantity in self.products.items():
            string += ' %s – %s stk\n' % (product.sn, quantity)
        
        string += 'Total weight: %s kg' % self.get_total_weight()
        return string
    
    
    def get_total_weight(self):
        weight = 0
        for product in self.products.keys():
            weight += product.weight * self.products[product]
        
        return weight
    
    def addProduct(self, product, quantity):
        # TODO: check if delivery already has the product, in that case only increase quantity
        self.products[product] = self.products[product] + quantity

        
    def removeProduct(self, product, quantity):
        self.products[product] = self.products[product] - quantity
        if  self.products[product] <= 0:
            del  self.products[product]


    




class Cell:
    # Possible types
    MOVE = 'M'
    STORAGE = 'S'
    LOAD = 'L'

    # Possible directions
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    directions = {UP: 'U', DOWN: 'D', LEFT: 'L', RIGHT: 'R'}
    
    def  __init__(self, type, x, y, direction =  None, shelves = None) -> None:
        # type = (storage cells, route cells, loading/unloading cells)
        # if route cell, direction is needed
        # if storage cell,shelves are needed
        self.type = type
        self.x = x
        self.y = y
        self.direction = direction # Beste måten å lagre retning på?
        self.shelves = {} # dictionary with shelves, exactly 2 (maybe array is not the best way to store shelves)
        # {shelf1: [product1, product2, ..], shelf2: [product1, product2, ...]} Max weight per shelf: ??
        # TODO: make sure the selves does not overwrite 
   
    def addProductsToShelf(self):
        # {product1: quantity, product2: quantity} Max weight per shelf: 100 kg
        if len(self.shelves.keys()) < 2:
            # adds it to the shelf
            self.shelves[product] = 1
        if product in self.shelves.keys():
            # check if it is room for one more
            self.shelves[product] = self.shelves[product] + 1 
    
    def removeProductsToShelf(self):
        # {product1: quantity, product2: quantity} Max weight per shelf: 100 kg
        if product in self.shelves.keys():
            self.shelves[product] = self.shelves[product] - 1
            if self.shelves[product] == 0:
                del self.shelves[product]

    def canAddProduct(self, product):
        # Must check if a shelf is available 
        # Can only be one type per shelf, and max weight is 100kg

        # Step 1:
        # check if a shelf is empty
        if len(self.shelves.keys()) < 2:
            # adds it to the shelf
            return True
            self.shelves[product] = 1
        if product in self.shelves.keys():
            # check if it is room for one more
            return product.weight * self.shelves[product] + 1 <= 100

    def containsProduct(self, product):
        return product in self.shelves.keys()
        

    
    def printCellCord(self):
        '''
        prints a cell with x and y coordinate

        [ x, y]
        '''
        extra_x = ''
        extra_y = ''
        if self.x < 10:
            extra_x = '0'
        if self.y < 10:
            extra_y =  '0'
        
        return '[%s%s,%s%s]'  % (extra_x, self.x,  extra_y,self.y)
    
    def printCellType(self):
        '''
        prints the cell according to the type
        move:    [ U ] with the direction î
        load:    [   ]
        storage: [ X ]

        '''
        if self.type == self.MOVE:
            return '[ %s ]' % self.directions[self.direction]
        elif self.type == self.LOAD:
            return '[   ]'
        else:
            return '[ X ]'

        
class Truck:
    def __init__(self, deliveries) -> None:
        self.deliveries = deliveries #array of deliveries


class ClientOrder:
    def __init__(self, orders) -> None:
        self.orders = orders # a dictionary on the format {product1: quantity, product2: quantity, ...}
    
    def __str__(self) -> str:
        string = 'Delivery \n created at: %s \n' % self.created_at
        
        for product, quantity in self.products.items():
            string += ' %s – %s stk\n' % (product.sn, quantity)
        
        string += 'Total weight: %s kg' % self.get_total_weight()
        return string
    
    
    def get_total_weight(self):
        weight = 0
        for product in self.products.keys():
            weight += product.weight * self.products[product]
        
        return weight
    
    def add_product(self, product, quantity):
        if product in self.orders.keys():
            self.orders[product] = self.orders[product] + quantity
        else:
            self.orders[product] = quantity
        
    def remove_product(self, product, quantity):
        if quantity < self.orders[product]:
            self.orders[product] = self.orders[product] - quantity
        if quantity == self.orders[product]:
            del self.orders[product]
        else:
            #TODO: throw error for trying to remove more products than exists in the order
            
            pass
        

    


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
                    s += 'o'
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