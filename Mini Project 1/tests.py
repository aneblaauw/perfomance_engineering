# Testing Markovik Chains.

# Here is the tests we used while working with the assignment.
# Some tests were mandatory, but we decided to make others to test,
# as we had an top-down approach to this assignment, making sure the earlier finished tasks
# still worked correctly, when completing the future tasks.

import unittest
from models import ProbabilityDistribution, DTMC
from markov_chain import MarkovChain
from utils import tokenizeFile, generate_next_name
import numpy as np

class Test(unittest.TestCase):
    """Task 4. Prepared benchmark of DTMC and probability distributions."""
    def setUp(self):
        # the states
        self.states = ['CALM', 'MODERATE', 'ROUGH']

        # possible sequences of events
        self.transistionName = [['CC', 'CM', 'CR'], # CALM
                               ['MC', 'MM', 'MR'],  # MODERATE
                               ['RC', 'RM', 'RR']]  # ROUGH

                
        # Probabilities matrix (transition matrix)
        self.transitionMatrix = [[0.6, 0.4, 0.0], # CALM
                                [0.6, 0.3, 0.1],  # MODERATE
                                [0.0, 0.9, 0.1]]  # ROUGH

        self.probabilities = [1.0, 0.0, 0.0] # one probability for each state

        self.dtmc = DTMC('SeaCondition', self.states, self.transitionMatrix)
        self.p0 = ProbabilityDistribution('p0', self.dtmc, self.probabilities)
        self.mc = MarkovChain([self.dtmc], [self.p0])
        self.tokens = tokenizeFile('text_files/SeaCondition.txt')

    def test_create_DTMC(self):
        self.assertEqual(self.dtmc.name,'SeaCondition')
        self.assertEqual(self.dtmc.states, self.states)
        self.assertEqual(self.dtmc.transitions, self.transitionMatrix)
    
    def test_validation_DTMC(self):
        '''
        self.assertRaises(DTMC('Test', states=['we', 'we', 'we'], transitions=[[1, 2, 3], [0, 0, 0], [1]]), AssertionError)
        self.assertRaises(DTMC('Test', states=['we', 'we', 'we'], transitions=[[1, 0, 0], [0, 0, 0], [1]]), AssertionError)
        '''
    
    def test_validation_ProbabilityDistribution(self):
        # self.assertRaises(ProbabilityDistribution('Test', self.dtmc, [2.3]), AssertionError)
        pass

    def test_create_ProbabilityDistribution(self):        
        self.assertEqual(self.p0.name, 'p0')
    
    def test_create_MarkovChain(self):
        self.assertEqual(len(self.mc.DTMC_list), 1)
        self.assertEqual(len(self.mc.probability_distributions), 1)
    
    def test_MarkovChain_write_to_file(self):
        f  = self.mc.write_to_file('test.txt')
        self.assertEqual(f.name, 'text_files/test.txt')

    def test_parse_tokens(self):
        mc2 = MarkovChain()
        mc2.parse_tokens(tokens=self.tokens)

        # checking the DTMC created from the tokens
        self.assertEqual(self.mc.DTMC_list[0].name, 'SeaCondition')
        self.assertListEqual(mc2.DTMC_list[0].states, self.dtmc.states)
        np.testing.assert_array_equal(mc2.DTMC_list[0].transitions, self.dtmc.transitions)

        # checking the probability distribution
        self.assertEqual(self.mc.probability_distributions[0].name, self.p0.name)
        self.assertEqual(self.mc.probability_distributions[0].DTMC, self.p0.DTMC)
        self.assertEqual(self.mc.probability_distributions[0].probabilities, self.p0.probabilities)
    
    def test_generate_next_name(self):
        self.assertEqual(generate_next_name('p0'), 'p1')
    
    def test_Timeseries(self):
        timeseries = self.mc.timeSeries(self.dtmc, 'CALM', 5)
        print(timeseries)
    
    def test_DTMC_from_Timeseries(self):
        timeseries = self.mc.timeSeries(self.dtmc, 'CALM', 40)
        success, dtmc = self.mc.createDTMCfromTimeSeries(timeseries, self.states)
        print(success)
        while not success:
            timeseries = self.mc.timeSeries(self.dtmc, 'CALM', 40)
            success, dtmc = self.mc.createDTMCfromTimeSeries(timeseries, self.states)
        
        print(dtmc)
        print('States: ', dtmc.states)
        print('TransitionsMatrix: ', dtmc.transitions)
    
    def test_length_Timeseries(self):
        self.mc.timeSeriesToDTMC(self.dtmc)
    

if __name__ == '__main__':
    unittest.main()

