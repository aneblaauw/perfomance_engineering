# Contains the objects of the program, and their corresponding management methods.
# Contains also a class and corresponding methods to generate a report for the Kaplan-Meier estimations.

from importlib.resources import path
from re import U
from matplotlib import units
import matplotlib.pyplot as plt
from kaplan_meier import Calculator
from kaplan_meier import KaplanMeierEstimator
from utils import listFiles
from utils import readFile, dateToString
import numpy as np
import pandas as pd
import xlsxwriter
import os

"""Task 4. Class Database and class Unit are designed to record
reliability data loaded from Excel sheets.
"""
class DataBase:
    """
    The database consists of a dictionary with different units. Each unit is a specific component.
    The 10 different components are the following:
     - Temperature sensors (electronical); 
     - Pressure sensors (electronical); 
     - Vibration sensors (electronical); 
     - Acquisition modules (electronical); 
     - Logic solvers (electronical); 
     - Solenoid valves (mechanical);
     - Shutdown valves (mechanical); 
     - Motor pumps of type 1, 2 and 3 (mechanical). 
    """

    # This will be the keys in the dictionary to manage the units. 
    # The keys are the first three letters of the code for the different types of units.
    TEMPERATURE_SENSOR = 'TPS'
    PRESSURE_SENSOR =  'PRS'
    VIBRATION_SENSOR = 'VBS'
    AQUISITION_SENSOR  = 'AQM'
    LOGIC_SOLVER = 'LGS'
    SOLENOID_VALVES = 'SLV'
    SHUTDOWN_VALVES = 'SDV'
    MOTOR_PUMP1 = 'MP1'
    MOTOR_PUMP2 = 'MP2'
    MOTOR_PUMP3 = 'MP3'
    
    def __init__(self):
        """initialises the database. Units is set as an dictionary with keys being every component of different units. 
        Every component has a list with units of that type.
        """
        self.units = {self.TEMPERATURE_SENSOR :[],
                    self.PRESSURE_SENSOR: [],
                    self.VIBRATION_SENSOR: [],
                    self.AQUISITION_SENSOR: [],
                    self.LOGIC_SOLVER: [],
                    self.SOLENOID_VALVES: [],
                    self.SHUTDOWN_VALVES: [],
                    self.MOTOR_PUMP1: [],
                    self.MOTOR_PUMP2: [],
                    self.MOTOR_PUMP3: []
                    }
    
    def createDataBase(self, dir_path=os.path.dirname(os.path.realpath(__file__)), foldername="/ReliabilityData"):
        """Creates a database from a folder with many (or one) worksheets.
        """
        files = listFiles(dir_path + foldername)
        for file in files:
            self.addUnits(dir_path + foldername+'/'+ file)
    

    def addUnits(self, file):
        """Reads from an excel file and creates a unit from every row in the file. 
        The unit will be added to the databases units-dictionary according to the component.

        Args:
            file (str): The name of the file to be read
        """
        df = readFile(file)
        for i, row in df.iterrows():
            unit = Unit(row['Code'], row['Description'], row['In-Service Date'], row['Out-Service Date'], row['Failure Date'])
            key = unit.code[0:3]
            self.units[key].append(unit)


    def printUnits(self, filename='Test.xlsx'):
        """Task 5. Prints a dictionary of units to an excel file.

        Args:
            filename (str, optional): the name (and path) for the file. 
            Must end with .xlsx. Defaults to 'Test.xlsx'.
        """
    
        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        # Keep track of which cell no the different categories have
        worksheet.write(0, 0, 'Code')
        worksheet.write(0, 1, 'Description')
        worksheet.write(0, 2, 'In-Service Date')
        worksheet.write(0, 3, 'Out-Service Date')
        worksheet.write(0, 4, 'Failure Date')
        
        row = 1 # counts what row we are writing on
        for units in self.units.values():
            for unit in units:
                # write to excel 
                # the column for the different attributes must match the header created above
                worksheet.write(row, 0, unit.code)
                worksheet.write(row, 1, unit.description)
                worksheet.write(row, 2, dateToString(unit.in_service_date))
                worksheet.write(row, 3, dateToString(unit.out_service_date))
                worksheet.write(row, 4, dateToString(unit.failure_date))
                row += 1
        workbook.close()


class Unit:
    """Data structure for a unit."""
    def __init__(self, code, description, in_service_date, out_service_date, failure_date):
        self.code = code
        self.description = description
        self.in_service_date = in_service_date
        self.out_service_date = out_service_date
        self.failure_date = failure_date


class ReportGenerator:
    """Task 9. Class to generate semi-automatically the HTML pages from the data base'
    """
    def __init__(self, database, name='plants'):
        self.database = database
        self.name = name
    
    def convert_to_HTML(self, filename='report', dir_path=os.path.dirname(os.path.realpath(__file__)) + '/analysis/'):
        # TODO: fix format html
        # TODO: fix """" mistake
        # TODO: generate real name for each component, not only code
        data = "<html> \n <h1>Report for data base</h1>"

        for component in self.database.units.keys():
            component_title = KaplanMeierEstimator.COMPONENTS[component]
            data += "\n <h2><p>Kaplan-Meier estimate: " + component_title + "</p></h2>"
            data += "\n </br>"
            data += "\n <img src='../analysis/survival_analysis_" + component + ".png' />"
        # Assumes the png plot alretady exists
        # TODO: find the path for the component
        data += "\n </html>" # close the tags
        
        with open(dir_path + filename + ".html", "w") as file:
            file.write(data)
            file.close()

