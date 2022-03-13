# helping functions to manage the different objects

import os
import pandas as pd

from datetime import datetime


def listFiles(path):
    """Task 1. Function that lists all of the files contained in a folder
    
    Args:
        path (string): path for the files to be listed
    
    Returns:
        
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
        date (dateTime): The date created from the string
    """

    datetime_object = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')

    return datetime_object

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
