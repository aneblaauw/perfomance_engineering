
import unittest

from utils import createCatalog, createRandomDelivery, createTruckLoading, createWareHouse
from warehouse import findAlley
from models import Delivery, Truck, Cell
import random

class Test(unittest.TestCase):
    def setUp(self):
        self.catalog = createCatalog()
        self.warehouse = createWareHouse(5, 5)
        self.warehouse.addRobots(1)


    def test_createCatalog(self):
        n = 5
        catalog = createCatalog(n)
        self.assertEqual(n, len(catalog.products))
    
    def test_Delivery(self):
        dict = {}
        for i in range(5):
            index = random.randint(0, len(self.catalog.products) -1)
            quantity = random.randint(1,5)
            #print(quantity)
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
            #print(delivery)
            deliveries.append(delivery)
        
        truck = createTruckLoading(deliveries, max_weight=500)
        '''
        print('Deliveries in truck')
        for delivery in truck.deliveries:
            print(delivery)
        '''
        
    def test_createWareHouse(self):
        floor_map = []
        floor_map = addAlley(floor_map=floor_map)
        # TODO: find way to actually add the alley to the floor map
        #printFloorMap(floor_map)
    
    def test_createWareHouse(self):
        warehouse = createWareHouse(5,5)
        #printFloorMap(warehouse.floor_map)
        #print(warehouse.catalog)
    
    def test_CalculateRoute(self):
        cell1 = Cell('S', 1,1)
        route1 = self.warehouse.calculateRoute(cell1,self.warehouse.robots[0])
        correct1 = [[0, 8], [1, 8], [2, 8], [3, 8], [3, 7], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [2, 1], [1, 1], [2, 1], [3, 1], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [3, 9], [2, 9], [1, 9], [0, 9]]
        self.assertEqual(route1, correct1)

        cell2 = Cell('S', 6,1)
        route2 = self.warehouse.calculateRoute(cell2,self.warehouse.robots[0])
        correct2 = [[0, 8], [1, 8], [2, 8], [3, 8], [3, 7], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [4, 1], [5, 1], [6, 1], [5, 1], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [3, 9], [2, 9], [1, 9], [0, 9]]
        self.assertEqual(route2, correct2)

        cell3 = Cell('S', 6,16)
        route3 = self.warehouse.calculateRoute(cell3,self.warehouse.robots[0])
        correct3 = [[0, 8], [1, 8], [2, 8], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [3, 15], [3, 16], [4, 16], [5, 16], [6, 16], [5, 16], [4, 16], [4, 15], [4, 14], [4, 13], [4, 12], [4, 11], [4, 10], [4, 9], [3, 9], [2, 9], [1, 9], [0, 9]]
        self.assertEqual(route3, correct3)
    def test_findAlley(self):
        # All cells between 1 and 6 should belong to alley 1
        self.assertEqual(1, findAlley(1))
        self.assertEqual(1, findAlley(2))
        self.assertEqual(1, findAlley(3))
        self.assertEqual(1, findAlley(4))
        self.assertEqual(1, findAlley(5))
        self.assertEqual(1, findAlley(6))

        # All cells between 7 and 12 should belong to alley 2
        self.assertEqual(2, findAlley(7))
        self.assertEqual(2, findAlley(10))
        self.assertEqual(2, findAlley(12))

        # All cells between 13 and 18 should belong to alley 3
        self.assertEqual(3, findAlley(13))
        self.assertEqual(3, findAlley(15))
        self.assertEqual(3, findAlley(18))


    def test_calculateRoute2(self):
        # calculate route for warehouses with  many alleys
        cell1 = Cell('S', 7,1)
        route1 = self.warehouse.calculateRoute(cell1,self.warehouse.robots[0])
        #correct1 = [[0, 8], [1, 8], [2, 8], [3, 8], [3, 7], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [2, 1], [1, 1], [2, 1], [3, 1], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [3, 9], [2, 9], [1, 9], [0, 9]]
        #self.assertEqual(route1, correct1)
        print(route1)







if __name__ == '__main__':
    unittest.main()