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
    
    def add_product(self, product, quantity):
        # TODO: check if delivery already has the product, in that case only increase quantity
        self.products[product] = quantity
        
    def remove_product(self, product, quantity):
        # TODO: fix
        # lower the quantity
        self.products.remove(product[quantity])
    

class Robot:
    # can carry products of only one type at a time, but no more than 40kg
    def __init__(self, ) -> None:
        pass


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
        # {shelf1: [product1, product2, ..], shelf2: [product1, product2, ...]} Max weight per shelf: ??
        # TODO: make sure the selves does not exeed max weight
        pass
    
    def printCellCord(self):
        '''
        prints a cell with x and y coordinate

        [ x, y]
        '''

        return '[%s,%s]'  % (self.x,  self.y)
    
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


class Shelf:
    def __init__(self, product, quantity) -> None:
        # total weights of products stored on a shelf cannot exceed 100kg
        self.product = product
        self.quantity = quantity
        

class Warehouse:
    def __init__(self, floor_map, catalog, robots) -> None:
        self.floor_map = floor_map # an double linked array of cells, where cells are placed according to coordinates
        self.catalog = catalog
        self.robots = robots # array of robots,maybe not needed in initializing
        self.client_orders = [] # client orders is added along the way

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

    def add_alley(self, size):
        # code in function "addAlley" in utils.py
        pass

    def addClientOrders(self, order):
        self.client_orders.add(order)

    def addClientOrders(self, order):
        self.client_orders.remove(order)
        
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
            #TODO: throw error for trying  to removemore products than exists in the order
            pass
        

    


class Printer:
    """Task3. In charge of printing all info related to the warehouse
    and its operation.
    """
    
    pass