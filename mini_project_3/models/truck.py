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



