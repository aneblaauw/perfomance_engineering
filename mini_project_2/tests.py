# Contains functions that to test that all the functionalities
# implemented in the program is working correctly.

import string
import unittest
import os
from kaplan_meier import KaplanMeierEstimator, Calculator
from utils import listFiles, readFile, stringToDateTime, calculateTimeDifference, dateToString, calculateSurvivalTimes
from models import DataBase, ReportGenerator

class Test(unittest.TestCase):
    def setUp(self):
        self.dataBase = DataBase()
        self.dataBase.createDataBase(foldername='/TestFiles')

    def test_listFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = listFiles(dir_path + "/TestFiles")
        self.assertEqual(len(files), 2)
        self.assertTrue('Plant1_test.xlsx' in files)

    def test_readFile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = 'Plant1_test.xlsx'
        dataFrame = readFile(dir_path +"/TestFiles/" + filename )
        self.assertEqual(len(dataFrame), 9)
        self.assertEqual(dataFrame.columns[0], 'Code')
    
    def test_stringToDate(self):
        date_string = '2021-02-14 14:00:00'
        dateTimeObj = stringToDateTime(date_string)
        self.assertEqual(dateTimeObj.month, 2)
        self.assertEqual(dateTimeObj.year, 2021)
        self.assertEqual(dateTimeObj.day, 14)
        self.assertEqual(str(dateTimeObj.time()), '14:00:00')

    def test_dateToString(self):
        date_string = '2021-02-14 14:00:00'
        dateTimeObj = stringToDateTime(date_string)
        s = dateToString(dateTimeObj)
        self.assertEqual(s, date_string)

        #  testing for NaT values
        nat = 'NaT'
        s = dateToString(nat)
        self.assertEqual('', s)

    def test_timeDifference(self):
        start = stringToDateTime('2021-02-14 14:00:00')
        end = stringToDateTime('2021-02-15 14:00:00')
        difference = calculateTimeDifference(start, end)
        self.assertEqual(difference, 24)
        # sets a different end date
        end = stringToDateTime('2021-02-14 16:00:00')
        difference = calculateTimeDifference(start, end)
        self.assertEqual(difference, 2)

    def test_DataBase(self):
        self.assertEqual(len(self.dataBase.units[self.dataBase.PRESSURE_SENSOR]), 2)
        self.assertEqual(self.dataBase.units[self.dataBase.PRESSURE_SENSOR][0].code, 'PRS-001-00001')

        # Testing creating units from a folder
        self.assertEqual(len(self.dataBase.units[self.dataBase.MOTOR_PUMP2]), 3)

        # testing printing to excel
        self.dataBase.printUnits()
    
    def test_CalculateSurvival(self):
        units = self.dataBase.units[self.dataBase.MOTOR_PUMP2]
        survival = calculateSurvivalTimes(units)

        self.assertEqual(survival, [4885.0, 7313.0, 8760.0])
    
    def test_KaplanMeierEstimator(self):
        kp_estimator = KaplanMeierEstimator(self.dataBase.MOTOR_PUMP2, self.dataBase.units[self.dataBase.MOTOR_PUMP2])
        self.assertEqual(kp_estimator.durations, [4885.0, 7313.0, 8760.0])
        kp_estimator.survivalFunction()
    
    
    def test_Calculator(self):
        # creating the real database
        real_db = DataBase()
        real_db.createDataBase()

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
        
        components = [TEMPERATURE_SENSOR,
                PRESSURE_SENSOR,
                VIBRATION_SENSOR,
                AQUISITION_SENSOR,
                LOGIC_SOLVER,
                SOLENOID_VALVES,
                SHUTDOWN_VALVES,
                MOTOR_PUMP1,
                MOTOR_PUMP2,
                MOTOR_PUMP3]

        calculator = Calculator(real_db, components[9])
        survival = calculator.kme.survivalFunction()
        calculator.plotAndSave()
    
    
    def test_ReportGenerator(self):
        # testing that a report is generated
        generator = ReportGenerator(self.dataBase)
        generator.convert_to_HTML()
    


if __name__ == '__main__':
    unittest.main()