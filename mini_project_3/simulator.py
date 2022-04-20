# handles the operation of the warehouse


from utils import createWareHouse
from models import Cell, ClientOrder, Printer
from warehouse import Warehouse
from robot import Robot




warehouse = createWareHouse(2,1)
printer = Printer(warehouse)

printer.printFloorMap()
printer.printFloorMapCord()

warehouse.addRobots(1)
printer.printFloorMap()



    

    
