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