# MarkovChain class

# Has functions to do:
# reading and writing DTMC and probability distributions,
# calculations regarding DTMC,
# build a DTMC from a time series and vice-versa.

from models import DTMC, ProbabilityDistribution
import numpy as np
from utils import generateDTMCfromTokens, generateProbDistFromTokens, generate_next_name, nextState


class MarkovChain():
    """Task 3. Data structure to manage one DTMC with an unknown number of probability distributions"""
    def __init__(self, DTMC=[], probability_distributions=[]):
        self.DTMC_list = DTMC
        self.probability_distributions = probability_distributions
    
    def __str__(self):
        DTMC_str = [dtmc.name for dtmc in self.DTMC_list]
        probability_dist_str = [pd.name for pd in self.probability_distributions]
        return f'MarkovChain(DTMCs=%s, ProbabilityDistributions=%s)' % (DTMC_str, probability_dist_str)

 
    def write_to_file(self, filename):
        """Task 5. Function that prints a list of DTMC and a list of probability
        distributions into a file.

        Args:
            filename (file.txt): filename that is being written into

        Returns:
            (file.txt): written file
        """
        path = 'text_files/'
        f = open(path + filename, 'w')
        # writing the DTMCs
        for DTMC in self.DTMC_list:
        
            f.write('MarkovChain ' + DTMC.name+ "\n") 
            # writing the states
            for i in range(len(DTMC.states)):
                for j in range(len(DTMC.states)):
                    f.write("\t" + DTMC.states[i] + " -> " + DTMC.states[j]+": " + str(DTMC.transitions[i][j]) + ";\n")
            
            f.write("end \n \n")

        # writing the probability distributions
        for dist in self.probability_distributions:
            f.write('ProbabilityDistribution ' + str(dist.name) + " of " + str(dist.DTMC.name) + '\n')
            for i in range(len(dist.probabilities)):
                f.write('\t' + dist.DTMC.states[i] + ': ' + str(dist.probabilities[i]) + ';\n')
            f.write('end \n \n')
        f.close

        return f

   
    def parse_tokens(self, tokens):
        '''Task 8. Parses a list of tokens to DTMCs or probability distributions.
           Uses help functions found in utils.py.'''
        start_index = 0
        end_index = 0
        while start_index < len(tokens):
            try:
                end_index = start_index + [ token.string for token in tokens[start_index:] ].index('end')
            except ValueError:
                print('Tokens list must contain an "end" token')
            
            group = tokens[start_index:end_index + 1]
            
            # the first token in a new group defines the type of the group
            if group[0].string == 'MarkovChain':
                DTMC = generateDTMCfromTokens(group[1:])
                self.DTMC_list.append(DTMC)

            
            elif group[0].string == 'ProbabilityDistribution':
                probability_dist = generateProbDistFromTokens(self, group[1:])
                self.probability_distributions.append(probability_dist)
            
            start_index = end_index + 1
    
    
    def computeNextStep(self, pi, dtmc):
        '''Task 10. Implement a function that calculates the product of a probability distribution by the
        sparse matrix (calculates the next step).
        
        Args:
           pi (int): the probability at a given step
           dtmc (DTMC): the DTMC
        '''
        M = dtmc.transitions
        p = pi @ M

        new_name = generate_next_name(pi.name)

        p_new = ProbabilityDistribution(new_name, dtmc, p) # name is dependent on the previos step, ex. pi = p1 -> p_new = p2
        
        self.probability_distributions.append(p_new)
    
    def sojournTimes(dtmc, p0, n):
        '''Task 11. Implement functions that, given a DTMC and an initial probability distribution,
        calculate the probability distribution and the sojourn times in each state after a
        mission of n steps.
        
        Args: 
            DTMC (DTMC): the DTMC
            p0 (int): the initial probability
            n (int): number of steps
        '''
        # the probaiblity at step i, given M and p0 is...
        M = DTMC.transitionMatrix
        M_ = p0 @ M
        for i in range(n):
            M_ = M_ @ M

        return M

    def timeSeries(self, dtmc, s0, n):
        """Task 12. Generates a time series from a DTMC.

        Args:
            dtmc (DTMC): a DTMC
            s0 (string): intial state
            n (int): number of steps
        
        Returns:
            timeseries ([string]): the timeseries generated
        """
        currentState = s0
        timeSeries = [currentState]
        for k in range(n): # number of steps 
            timeSeries= nextState(timeSeries, dtmc)

        return timeSeries

    def createDTMCfromTimeSeries(self, timeseries, possibleStates, name='test'):
        """Task 13. Creates a DTMC using frequencies of transitions between states in a time series.
            Assumes the timeseries has every possible state present

        Args;
            timeseries ([string]): The timeseries, an array with states 
            possibleStates ([styring]): The different states the DTMC can have
            name (string): The name for the DTMC

        Returns:
            bool: True if a DTMC was created, False otherwise
            dtmc: the DTMC created from the timeseries
        """
        
        transitionMatrix = []  
        transitions = { s: { next_s : 0 for next_s in possibleStates} for s in possibleStates } # the different states and their next possible state
        
        for i in range(len(timeseries)-1):
            fromState = timeseries[i]
            toState = timeseries[i+1]
            transitions[fromState][toState] = transitions[fromState][toState] +1


        for state_from in possibleStates:
            totalOut = sum(transitions[state_from].values())
            if totalOut == 0: 
                return False, None
            stateTransitions = []
            for state_to in possibleStates:
                value = transitions[state_from][state_to] / totalOut
                stateTransitions.append(value)
            transitionMatrix.append(stateTransitions)
        
            
        dtmc = DTMC(name,possibleStates,transitionMatrix)
        return True, dtmc

  
    def timeSeriesToDTMC(self, dtmc, error=0.1, min_step=40, max_step=50000):
        """Task 14. Generates a timeseries from a dtmc, and finds the needed number of steps in order to 
            get a DTMC created from the timeseries close to the original

        Args:
            dtmc (DTMC): The DTMC for validation
            error (int, optional): The allowed error between the generated timeseries and the original
            min_step (int): Number of minimum steps
            max_step (int): Number of maximum steps
        Returns:
            success (bool): success or not
            n (int): number of steps used
            dtmc_new (DTMC): DTMC generated from the time series 
        """
        assert min_step > 0 , f'min_step can not be smaller than 0'
        assert max_step > min_step, f'max_step must be bigger than min_step'

        # first generate a timeseries from the DTMC, the smallest number of steps is 40
        timeseries = self.timeSeries(dtmc, dtmc.states[0], min_step)
        success, dtmc_new = self.createDTMCfromTimeSeries(timeseries, dtmc.states, name='Generated from timeseries')
        while not success:
            timeseries = self.timeSeries(dtmc, dtmc.states[0], min_step)
            success, dtmc_new = self.createDTMCfromTimeSeries(timeseries, dtmc.states, name='Generated from timeseries')

        n = min_step
        # np.allclose returns True if two arrays are element-wise equal within a tolerance
        while not np.allclose(dtmc.transitions, dtmc_new.transitions, error) and n < max_step: 
            timeseries = nextState(timeseries, dtmc)
            success, dtmc_new = self.createDTMCfromTimeSeries(timeseries, dtmc.states, name='Generated from timeseries')
            print('success: ', success)
            print('Length of timeseries: ', len(timeseries))
            print('New transitionMatrix: \n')
            dtmc_new.printTransitions()
            print('\n \n')
            n += 1
        success = np.allclose(dtmc.transitions, dtmc_new.transitions, error)
        print('number of iterations: ', n)
        print('Alike: ', np.allclose(dtmc.transitions, dtmc_new.transitions, error) )
        
        print('Original transitionMatrix: \n', dtmc.printTransitions())
        print('New transitionMatrix: \n', dtmc_new.printTransitions())
        return success, n, dtmc_new


        









        
    
