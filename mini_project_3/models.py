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
            raise Exception("Product weight is either too light or too heavy.")
    
    def __str__(self) -> str:
        return self.sn

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
        if product not in self.products:
            self.products[product] = self.products[product]
        else:
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
        if self.type == self.STORAGE:
            self.shelves = {'shelf1': {}, 'shelf2': {}} # dictionary with shelves, exactly 2 (maybe array is not the best way to store shelves)
        # {shelf1: {product: quntity}, shelf2: {product: quntity}} 
        else:
            self.shelves =  None
        
    def getProductsOnShelf(self):
        if self.type != self.STORAGE:
            raise Exception("Error, cell of type %s doesn't have shelves", self.type)
        else:
            products = []
            for shelf, items in self.shelves.items():
                for product in items.keys():
                    products.append(product)
            
            return products
   
    def addProductToShelf(self, product):
        # {shelf1: {product: quntity}, shelf2: {product: quntity}}   Max weight per shelf: 100 kg
        for shelf, products in self.shelves.items():
            # check if shelf is empty
            if not products:
                # add the product
                products[product] = 1
                #doesn't need to check the next shelf
                break
            else:
                # must check if it is the correct shelf
                if product in products.keys():
                    # assumes we have checked that the shelve can have the product
                    # add one to the shelf
                    products[product] =  products[product] + 1
                    #doesn't need to check the next shelf
                    break
        
        print('Product added to shelf!')
        print(self.printCellShelves())
    
    def removeProductFromShelf(self, product):
        #{shelf1: {product: quntity}, shelf2: {product: quntity}}   Max weight per shelf: 100 kg
        for shelf, products in self.shelves.items():
            if product in products.keys():
                products[product] = products[product] -1
                if products[product] == 0:
                    del products[product]
        print('Product removed from shelf!')
        print(self.printCellShelves())
                    

    def canAddProduct(self, product):
        # Must check if a shelf is available 
        # Can only be one type per shelf, and max weight is 100kg

        # Step 1:
        # check if a shelf is empty
        if len(self.getProductsOnShelf()) < 2:
            # has room for more products
            return True
        else:
            # check if the shelves has the correct type of products
            if product in self.getProductsOnShelf():
                # check if there is room for one more
                for shelf, products in self.shelves.items():
                    if product in list(products.keys()):
                        # calculate total weight for this shelf
                        total_weight = product.weight * products[product] +1
                        if total_weight <=100: #kg
                            # can add
                            return True
        return False

    def containsProduct(self, product):
        return product in self.getProductsOnShelf()
        

    def printCellCord(self):
        '''
        Prints a cell with x and y coordinate
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
        Prints the cell according to the type
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
            
    def printCellInfo(self):
        s = 'Cell %s \n' % self.printCellCord()
        if self.type == self.STORAGE:
            s+= 'Shelves:'
            s+= self.printCellShelves()
        return s
    
    def printCellShelves(self):
        s = ''
        if self.shelves is not None:
            for shelf in list(self.shelves.keys()):
                s = s + shelf + '\n'
                for product in self.shelves[shelf]:
                    print('Product: ', product)
                    total_weight = product.weight * self.shelves[shelf][product]
                    s+= 'Product: %s - %s stk \n Total weight: %s\n' % (product.sn, self.shelves[shelf][product], total_weight)
                    
        
        return s
                    
            

        
class Truck:
    MAX_WEIGHT = 20000 #kg
    def __init__(self, products={}) -> None:
        self.products = products # adictionary on format {product: quantity}

    def __str__(self) -> str:
        string = 'Truck: \n'
        
        for product, quantity in self.products.items():
            string += ' %s – %s stk\n' % (product.sn, quantity)
        
        string += 'Total weight: %s kg' % self.get_total_weight()
        return string
        

    def get_total_weight(self):
        weight = 0
        for product in self.products.keys():
            weight += product.weight * self.products[product]
        
        return weight
    
    def canAdd(self, product):
        return self.get_total_weight() + product.weight <= self.MAX_WEIGHT

    
    def add_product(self, product, quantity):
        
        if product in self.products.keys():
            self.products[product] = self.products[product] + quantity
        else:
            self.products[product] = quantity
        print('Product added to truck')
        print(self)
        
    def remove_product(self, product, quantity):
        if quantity < self.products[product]:
            self.products[product] = self.products[product] - quantity
        if quantity == self.products[product]:
            del self.products[product]
        else:
            raise Exception("Error, trying to remove more products than exists in the order.")



class ClientOrder:
    def __init__(self, orders) -> None:
        self.orders = orders # a dictionary on the format {product1: quantity, product2: quantity, ...}
        self.created_at = datetime.today()
    
    def __str__(self) -> str:
        string = 'Client Order \n created at: %s \n' % self.created_at
        
        for product, quantity in self.orders.items():
            string += ' %s – %s stk\n' % (product.sn, quantity)
        
        string += 'Total weight: %s kg' % self.getTotalWeight()
        return string
    
    def getTotalWeight(self):
        weight = 0
        for product in self.orders.keys():
            weight += product.weight * self.orders[product]
        
        return weight
    
    def addProduct(self, product, quantity):
        if product in self.orders.keys():
            self.orders[product] = self.orders[product] + quantity
        else:
            self.orders[product] = quantity
        
    def removeProduct(self, product, quantity):
        print('Trying to remove product from this order')
        print(self.orders[product])
        print(quantity)
        if quantity < self.orders[product]:
            self.orders[product] = self.orders[product] - quantity
        elif quantity == self.orders[product]:
            del self.orders[product]
        else:
            raise Exception("Error, trying to remove more products than exists in the order.")


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