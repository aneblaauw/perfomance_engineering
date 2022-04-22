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