import string
import unittest
import os
from utils import listFiles, readFile, stringToDateTime, calculateTimeDifference

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
    
    def test_timeDifference(self):
        start = stringToDateTime('2021-02-14 14:00:00')
        end = stringToDateTime('2021-02-15 14:00:00')
        difference = calculateTimeDifference(start, end)
        self.assertEqual(difference, 24)
        # sets a different end date
        end = stringToDateTime('2021-02-14 16:00:00')
        difference = calculateTimeDifference(start, end)
        self.assertEqual(difference, 2)

if __name__ == '__main__':
    unittest.main()