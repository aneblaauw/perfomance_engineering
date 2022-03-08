# Contains the objects of the program, 
# and their corresponding management methods.
# 

# Task 4 - record data loaded from Excel-files

from importlib.resources import path
import matplotlib.pyplot as plt
from utils import readFile
import numpy as np
import lifelines # vet ikke om vi trenger, er for plotting

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
        # TODO add keys to units andan empty array for each  value
        self.units = {self.TEMPERATURE_SENSOR :[],
                    self.PRESSURE_SENSOR: [],
                    self.VIBRATION_SENSOR: [],
                    self.AQUISITION_SENSOR: [],
                    self.LOGIC_SOLVER: [],
                    self.SOLENOID_VALVES: [],
                    self.SHUTDOWN_VALVES: [],
                    self.MOTOR_PUMP1: [],
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
            # TODO: add the unit to units, depending on the key


        # we know the order of the values in the excel file
        
        
    
    def printUnits(self):
        """Prints a dictionary of units to excel
        """
        

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
    def __init__(self) -> None:
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
    """Task 9. Class to generate semi-automatically the HTML pages from the data base"""
    def __init__(self) -> None:
        pass
