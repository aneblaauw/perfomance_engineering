from datetime import datetime
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
