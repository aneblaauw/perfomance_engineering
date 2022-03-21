from operator import index
from utils import calculateSurvivalTimes, preparePlotValues
import matplotlib.pyplot as plt


class KaplanMeierEstimator:
    """Task 6. 
    Kaplan-Meier estimator : a non-parametric statistic,
    estimates the survival function of time-to-event data.

    A Kaplan-Meier estimator records the number of surviving components in a given fleet as a
    function of the time. It is encoded as a number of points (time, number-of-survivors) ordered
    by time. E.g.
    (0, 10),(123, 9),(4562.3, 8),(4689.9, 7),(8701.2, 6)
    As components are used for a limited mission time, some of them may reach this mission time
    without failing, which is reflected in the above example by the fact that the last point of the
    estimator records 6 survivors.

    Every unique component will have their own Kaplan-Meier estimator.

    Attributes:
    component (str): The name of the component, uses the same codes as defined in the dataBase class
    units (array): An array of units objects
    durations (array): A list with numbers corresponding to the survival time of each unit in hours, in ascending order


    Needs:
        * infomration about the different components -> sorted by key?
        * ? Code for every component?
        * The survival time of every component
        * ? What if the component were taken out before it broke down?
        * ? A parameter saying wether the component actually broke down or were put out of service?

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

    COMPONENTS = {
        TEMPERATURE_SENSOR : 'Temperature sensors (electronical)',
        PRESSURE_SENSOR : 'Pressure sensors (electronical)',
        VIBRATION_SENSOR : 'Vibration sensors (electronical)',
        AQUISITION_SENSOR : 'Acquisition modules (electronical)',
        LOGIC_SOLVER : 'Logic solvers (electronical)',
        SOLENOID_VALVES: 'Solenoid valves (mechanical)' ,
        SHUTDOWN_VALVES: 'Shutdown valves (mechanical)',
        MOTOR_PUMP1: 'Motor pumps 1 (mechanical)',
        MOTOR_PUMP2: 'Motor pumps 2 (mechanical)',
        MOTOR_PUMP3: 'Motor pumps 3 (mechanical)',
    }


    def __init__(self, component, units):
        """initializes the estimator

        Args:
            component (str): The name of the component, uses the same codes as defined in the dataBase class
            units (array): An array of units
        """
        self.component = component
        self.units = units
        # TODO: durations a good name?
        self.durations = calculateSurvivalTimes(units)
    
    def __str__(self) -> str:
        return 'Kaplan Meier Estimator, type: %s' % self.COMPONENTS[self.component]
    

    # move to Calculator?
    def survivalFunction(self):
        """Creates a list of tuples with the time (in  hours?) and number of units alive. Uses the datapoints that already
        exists in durations list
        It is encoded as a number of points (time, number-of-survivors) ordered
        by time. E.g.
        (0, 10),(123, 9),(4562.3, 8),(4689.9, 7),(8701.2, 6)
        """
        total_alive = len(self.durations)
        unique_survival_times = list(set(self.durations))
        unique_survival_times.sort()
        survival_points = []
        for time in unique_survival_times:
            # at a given time, the total number of units alive equals the length og self.durations from that time and out

            total_alive = len(self.durations[self.durations.index(time):])
            survival_points.append((time, total_alive))
        
        return survival_points




class Calculator:
    """Task 7. Class with management methods to extract Kaplan-Meier estimator from a data base
    This class belongs to a DataBase and can contains functionality for creating Kaplan-Meier estimators for the different 
    components in the database
    """

    def __init__(self, database, component) -> None:
        """
        Args:
            database (DataBase): The database for the calculator
        """
        self.database = database
        units = self.database.units[component]
        self.kme = KaplanMeierEstimator(component, units)
        self.kme.survivalFunction()
    
    
    
    def plotKME(self):
        x, y = preparePlotValues(self)

        plt.plot(x, y)
        plt.title('Survival Analysis: '+ self.kme.COMPONENTS[self.kme.component])
        plt.xlabel('lifetime [h]')
        plt.ylabel('Percent survival')
        plt.show()
    
    def exportKMEtofile(self):
        # TODO, fix: multiplke lines in each picture
        x, y = preparePlotValues(self)
        plt.plot(x, y)
        plt.title('Survival Analysis: '+ self.kme.COMPONENTS[self.kme.component])
        plt.xlabel('lifetime [h]')
        plt.ylabel('Percent survival')
        
        
        plt.savefig('mini_project_2/analysis/survival_analysis_'+ self.kme.component+".png")
        #plt.show()

        return 'mini_project_2/analysis/survival_analysis_'+ self.kme.component+".png"



    
