# handles the operation of the warehouse

from utils import createWareHouse
from models import *

import random


warehouse = createWareHouse(1,5)
printer = Printer(warehouse)

printer.printFloorMap()
printer.printFloorMapCord()

warehouse.addRobots(1) # test for 1 robot
printer.printFloorMap()
printer.printCatalog()

""" 
The code below simulates: Creating a truck delivery, 
a robot unloading the truck, load the delivery to the correct shelf.
"""
dict = {}


# for multiple products
for i in range(5):
    index = random.randint(0, len(warehouse.catalog.products) -1)
    quantity = random.randint(1,5)
    product = warehouse.catalog.products[index]
    dict[product] = quantity
'''

# for one product
for product in warehouse.catalog.products:
    dict[product] = 5
'''

delivery = Delivery(dict)

# add this delivery to the warehouse, and begin unloading
# when a delivery is added, the available robots takes a product from the truck and places it in an available cell

warehouse.addDelivery(delivery)

robot = warehouse.robots[0] # the warehouse only has one robot per now
#print(robot.route)
#print(robot.currentLocation)
#print(robot.products)


# While there is a job to be done at the warehouse, the robots must work
while warehouse.jobToBeDone():
    for robot in warehouse.robots:
        warehouse.nextAction(robot)
    #printer.printFloorMap()

print('Delivery is finished unloading!')

"""
The code below simulates: Creating a client order, 
a robot picking up the delivery, and loading a delivery truck.
A client order is a delivery object, but it should be added to the client_orders list to the warehouse
"""

dict = {}


for i in range(3):
    index = random.randint(0, len(warehouse.catalog.products) -1)
    quantity = random.randint(1,5)
    product = warehouse.catalog.products[index]
    dict[product] = quantity

'''
for products in warehouse.catalog.products:
    dict[product] = 1
'''

client_order = ClientOrder(dict)

print('Client order added: ', client_order)

warehouse.addClientOrder(client_order)
robot = warehouse.robots[0] # the warehouse only has one robot per now
#print(robot.route)
#print(robot.currentLocation)
#print(robot.product_to_pick_up.sn)

while warehouse.jobToBeDone():
    for robot in warehouse.robots:
        warehouse.nextAction(robot)
    #printer.printFloorMap()


print('Truck is loaded with: \n', warehouse.deliveryTruck)





    
