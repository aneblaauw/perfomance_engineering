import string
import unittest
import os
from utils import listFiles, readFile, stringToDateTime, calculateTimeDifference, dateToString
from models import DataBase

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_listFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        files = listFiles(dir_path + "/ReliabilityData")
        self.assertEqual(len(files), 123)
        self.assertTrue('Plant1.xlsx' in files)

    def test_readFile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = 'Plant1.xlsx'
        dataFrame = readFile(dir_path +"/ReliabilityData/" + filename )
    
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
        dataBase = DataBase()

        # testing reading a file and adding units
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = 'Plant1.xlsx'
        dataBase.addUnits(dir_path +"/ReliabilityData/" + filename )
        '''
        for key, value in dataBase.units.items():
            print(key)
            for i in range(2):
                print(value[i].code)
                print(value[i].description)
                print(value[i].in_service_date)
                print(value[i].out_service_date)
                print(value[i].failure_date)
        '''

        # testing printing to excel
        dataBase.printUnits()


if __name__ == '__main__':
    unittest.main()