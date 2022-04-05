
import unittest
from utils import createCatalog, createRandomDelivery, createTruckLoading
from models import Delivery, Truck
import random

class Test(unittest.TestCase):
    def setUp(self):
        self.catalog = createCatalog()


    def test_createCatalog(self):
        n = 5
        catalog = createCatalog(n)
        self.assertEqual(n, len(catalog.products))
    
    def test_Delivery(self):
        dict = {}
        for i in range(5):
            index = random.randint(0, len(self.catalog.products) -1)
            quantity = random.randint(1,5)
            print(quantity)
            product = self.catalog.products[index]
            dict[product] = quantity
        #print(dict)
        delivery = Delivery(dict)
        #print(delivery)
        #print(self.catalog)
        #print(delivery.get_total_weight())
        # TODO: faktisk lag test
    
    def test_TruckLoad(self):
        # creates a couple of deliveries
        deliveries = []
        for i in range(3):
            delivery = createRandomDelivery(self.catalog)
            print(delivery)
            deliveries.append(delivery)
        
        truck = createTruckLoading(deliveries, max_weight=500)
        print('Deliveries in truck')
        for delivery in truck.deliveries:
            print(delivery)






if __name__ == '__main__':
    unittest.main()