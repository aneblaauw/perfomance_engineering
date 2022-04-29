# Contains helping functions to manage the different objects, and
# are used in other functions for calculations. 

import os
import pandas as pd
from datetime import datetime


def listFiles(path):
    """Task 1. Function that lists all of the files contained in a folder
    
    Args:
        path (string): path for the files to be listed
    
    Returns: files (file.txt): file to be listed
    """

    files = os.listdir(path)
    return files


def readFile(path):
    """Task 2. Reads an xlsx file and extracts the content. Assumes the file only has one sheet

    Args:
        path (string): path for the file to be read
    
    Returns:
        dataFrame (pandas DataFrame): a DataFrame with the data from the excel file
    """
   
    dataFrame = pd.read_excel(path)
    return dataFrame 

def stringToDateTime(string):
    """Task 3. Converts a string to a datetime object. 
    The string must be on this format 2021-02-14 14:00:00 

    Args:
        string (string): the string that should be converted
    
    Returns:
        date (dateTime): the date created from the string
    """

    datetime_object = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    return datetime_object

def dateToString(datetime_object):
    """Helping function to convert a date to string-format."""

    if str(datetime_object) == str('NaT'):
        return ''
    string = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
    return string


def calculateTimeDifference(startDate, endDate):
    """Task 3. Calculates the difference between two dates in hours.

    Args:
        startDate (Datetime): starting date
        endDate (Datetime): ending date
    Returns:
        hours (int): The hours between the dates
    """

    difference = endDate - startDate
    duration_in_s = difference.total_seconds() 
    hours = divmod(duration_in_s, 3600)[0] 
    return hours

def calculateSurvivalTimes(units):
    """Calculates the survival times of units."""
    durations = []
    for unit in units:
        # if str(unit.failure_date).:
        # We know that every unit has a in_service_date and either a failure_date or an out_service_date
        if str(unit.out_service_date) == 'NaT':
            # must use failure_date
            end_date = unit.failure_date
        else:
            end_date = unit.out_service_date
            # Should we use the out_service_date in the same way we use failure date?
        survival_time = calculateTimeDifference(unit.in_service_date, end_date)
        durations.append(survival_time)
        durations.sort()
        #survival_time = calculateTimeDifference(unit.in_service_date, unit.out_service_date)

    return durations

def preparePlotValues(calculator):

        sorted_durations = calculator.kme.durations
        survival_points = calculator.kme.survivalFunction()

        #unique_durations
        x = sorted(list(set(sorted_durations)))

        y = []
        for tup in survival_points:
            y.append(tup[1]/len(sorted_durations))
        return x, y
