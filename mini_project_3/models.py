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
        self.floor_map = floor_map # an double linked array of cells, where cells are placed according to coordinates
        self.catalog = catalog
        self.robots = robots # array of robots,maybe not needed in initializing

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
        '''
        Assumes an alley is a whole row (top to bottom)
        Adds an alley of given size to the warehouse  floor map
        An alley will always consist of exactly 2 x size of storage cells, 2x size load/unload cells and 2x move cells
        This will be the same for top and bottom, and we have to add the middle aisle
        Middle:
            - consists of 4 x 6 cells
        '''

        # Step 2, create the top ailse
        # TODO: find the coordinates for the middle and end of the warehouse
        x = None # the coordinates for the end of the warehouse
        y = None # The coordinates for the middle top

        # coordinates for the first storage cell
        x = x+1
        y = y-2
        for i in range(size):
            # create the storage cells
            storage1 = Cell('S',x,y)
            unload1 = Cell('L', x + 1, y)
            move1 = Cell('M', x + 2, y, direction='UP')

            
            move2 = Cell('M', x + 3, y, direction='DOWN')
            unload2 = Cell('L', x + 4, y)
            storage2 = Cell('S',x + 5,y)

            # TODO: add the cells to the floor map

            y = y-1
        
        # Step 2, create the bottom ailse
        # TODO: find the coordinates for the middle and end of the warehouse
        x = None # the coordinates for the end of the warehouse
        y = None # The coordinates for the middle bottom

        # coordinates for the first storage cell
        x = x+1
        y = y+2

        for i in range(size):
            # create the storage cells
            storage1 = Cell('S',x,y)
            unload1 = Cell('L', x + 1, y)
            move1 = Cell('M', x + 2, y, direction='UP')

            
            move2 = Cell('M', x + 3, y, direction='DOWN')
            unload2 = Cell('L', x + 4, y)
            storage2 = Cell('S',x + 5,y)

            # TODO: add the cells to the floor map

            y = y + 1
        
        # Step 4 create the middle
        # TODO: find the coordinates for the middle and end of the warehouse
        x = None # the coordinates for the end of the warehouse
        y = None # The coordinates for the middle top

        x = x+1

        for i in range(2):

            unload1 = Cell('L', x, y-1)
            unload2 = Cell('L', x +1, y-1)
            movetop1 = Cell('M', x+2, y-1,  direction='UP')
            movetop2 = Cell('M', x+3, y-1,  direction='DOWN')
            unload3 = Cell('L', x+4, y-1)
            unload4 = Cell('L', x +5, y-1)

            mover1 = Cell('M', x, y, direction='RIGHT')
            mover2 = Cell('M', x +1, y, direction='RIGHT')
            mover3 = Cell('M', x +2, y, direction='RIGHT')
            mover4 = Cell('M', x +3, y, direction='RIGHT')
            mover5 = Cell('M', x +4, y, direction='RIGHT')
            mover6 = Cell('M', x +5, y, direction='RIGHT')

            movel1 = Cell('M', x, y +1, direction='LEFT')
            movel2 = Cell('M', x +1, y +1, direction='LEFT')
            movel3 = Cell('M', x +2, y +1, direction='LEFT')
            movel4 = Cell('M', x +3, y +1, direction='LEFT')
            movel5 = Cell('M', x +4, y +1, direction='LEFT')
            movel6 = Cell('M', x +5, y +1, direction='LEFt')

            unloadbottom1 = Cell('L', x, y+2)
            unloadbottom2 = Cell('L', x +1, y+2)
            movebottom1 = Cell('M', x+2, y+2,  direction='UP')
            movebottom2 = Cell('M', x+3, y+2,  direction='DOWN')
            unloadbottom3 = Cell('L', x+4, y+2)
            unloadbottom4 = Cell('L', x +5, y+2)

            #TODO: add to floor_map








        
        pass
        
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