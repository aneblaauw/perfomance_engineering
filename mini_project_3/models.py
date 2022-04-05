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
        pass
    
    def remove_product(self, product, quantity):
        pass

class Robot:
    # can carry products of only one type at a time, but no more than 40kg
    pass

class Cell:
    def  __init__(self, type, x, y, direction =  None, shelves = None) -> None:
        # type = (storage cells, route cells, loading/unloading cells)
        # if route cell, direction is needed
        # if storage cell,shelves are needed
        self.type = type
        self.x = x
        self.y = y
        self.direction = direction # Beste måten å lagre retning på?
        self.shelves = shelves # an array with shelves, exactly 2 (maybe array is not the best way to store shelves)

class Shelf:
    def __init__(self, product, quantity) -> None:
        # total weights of products stored on a shelf cannot exceed 100kg
        self.product = product
        self.quantity = quantity
        

class Warehouse:
    def __init__(self, floor_map, catalog, robots) -> None:
        self.floor_map = floor_map # an array of cells
        self.catalog = catalog
        self.robots = robots # array of robots,maybe not needed in initializing
        
class Truck:
    def __init__(self, deliveries) -> None:
        self.deliveries = deliveries #array of deliveries


class ClientOrder:
    pass # venter litt

class Printer:
    """Task3. In charge of printing all info related to the warehouse
    and its operation.
    """
    
    pass