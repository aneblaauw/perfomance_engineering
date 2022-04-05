# Contains helping methods


from models import Catalog, Product, Truck, Delivery

import random
import string



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


