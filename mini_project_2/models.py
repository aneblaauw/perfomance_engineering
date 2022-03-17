# Contains the objects of the program, 
# and their corresponding management methods.
# 

# Task 4 - record data loaded from Excel-files

from importlib.resources import path
from re import U
from matplotlib import units
import matplotlib.pyplot as plt
from utils import readFile, dateToString
import numpy as np
import pandas as pd
#import lifelines # vet ikke om vi trenger, er for plotting
import xlsxwriter
#import xlwt
#from xlwt import Workbook

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

    # This will be the keys in the dictionary to manage the units, the keys are taken from the first three letters of the 
    # the code for the different types of units
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

    def addUnits(self, file):
        """
        Reads from an excel file and creates units and adds to the dictionary with units
        """
        df = readFile(file)
        for i, row in df.iterrows():
            unit = Unit(row['Code'], row['Description'], row['In-Service Date'], row['Out-Service Date'], row['Failure Date'])
            key = unit.code[0:3]
            self.units[key].append(unit)

        
    def printUnits(self, filename='Test.xlsx'):
        """Task 5. Prints a dictionary of units to an excel.
            filename (string): the name (and path)  for the file. Must en with .xlsx
        """

        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook('Test.xlsx')
        worksheet = workbook.add_worksheet()

        # holde styr på hvilken cellenr de forskjellige kategoriene har
        worksheet.write(0, 0, 'Code')
        worksheet.write(0, 1, 'Description')
        worksheet.write(0, 2, 'In-Service Date')
        worksheet.write(0, 3, 'Out-Service Date')
        worksheet.write(0, 4, 'Failure Date')
        
        # loope gjennom units. 
        row = 1 # counts what row we are writing on
        for units in self.units.values():
            for unit in units:
                # write to excel 
                # the column for the different attributes must match the header created abowe
                #TODO: create smarter method for handling attribute and columns?
                worksheet.write(row, 0, unit.code)
                worksheet.write(row, 1, unit.description)
                worksheet.write(row, 2, dateToString(unit.in_service_date))
                worksheet.write(row, 3, dateToString(unit.out_service_date))
                worksheet.write(row, 4, dateToString(unit.failure_date))
                row += 1
        workbook.close()


class Unit:
    def __init__(self, code, description, in_service_date, out_service_date, failure_date):
        self.code = code
        self.description = description
        self.in_service_date = in_service_date
        self.out_service_date = out_service_date
        self.failure_date = failure_date
        
        
class KaplanMeierEstimator:
    """Task 6. 
    Kaplan-Meier estimator : a non-parametric statistic,
    estimates the survival function of time-to-event data.
    """
    def __init__(self, t_i, ):
        t_i = None # a duration time
        d_i = None # number of events that happened at time t_i
        n_i = None # number of individuals known to have survived up to time t_i
        pass
    
    def survivalFunction():
        """
        sum i from t_i < t : 1 - d_i/n_i
        """
        pass


class Calculator:
    """Task 7. Class with management methods to extract Kaplan-Meier estimator from a data base"""
    def __init__(self) -> None:
        pass

    
    # Task 8. Methods to draw out Kaplan-Meier estimator from a data base. 
    
class ReportGenerator:
    """Task 9. Class to generate semi-automatically the HTML pages from the data base'
    Ikke testet, og usikker om det er dette de spør om.
    """
    def __init__(self):
        pass
    
    def convert_to_HTML(self):
        # iterate dict -> iterate values
        # add the "<td>" tag after each value & <tr> after each key into a string
        # <tabel> tags at the start and end
        # save the string into a file html
        data = ""
        for units in self.units:
            data += "<td>" + units + "</td>"
            for unit in units[units]:
                data += "<td>" + unit + "</td>"
            data += "<tr>"
        
        with open("html_file.html", "w") as file:
            file.write(data)

