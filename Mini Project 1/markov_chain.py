
from models import DTMC, ProbabilityDistribution
import numpy as np
from utils import generateDTMCfromTokens, generateProbDistFromTokens, generate_next_name

# Task 3
class MarkovChain():
    # assuming you want to manage one DTMC with an unknown number of probability distributions
    def __init__(self, DTMC=[], probability_distributions=[]):
        self.DTMC_list = DTMC
        self.probability_distributions = probability_distributions
    
    def __str__(self):
        DTMC_str = [dtmc.name for dtmc in self.DTMC_list]
        probability_dist_str = [pd.name for pd in self.probability_distributions]
        return f'MarkovChain(DTMCs=%s, ProbabilityDistributions=%s)' % (DTMC_str, probability_dist_str)

    # Task 5
    def write_to_file(self, filename):
        path = 'text_files/'
        f = open(path + filename, 'w')
        # first write the DTMCs
        for DTMC in self.DTMC_list:
        
            f.write('MarkovChain ' + DTMC.name+ "\n") 
            # writing the states
            # TODO: update for list of DTMCs
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

    # Task 8
    # This task uses help functions found in utils.py
    def parse_tokens(self, tokens):
        '''
        parses a list of tokens to DTMCs or Probability Distributions

        '''
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
    
    
    '''Task 10. Implement a function that calculates the product of a probability distribution by the
    sparse matrix.'''
    # Assuming the task is to calculate the next step
    def computeNextStep(self, pi, dtmc):
        '''
        dtmc: the DTMC
        pi: the probability at a given step
        '''
        M = dtmc.transitions #numpy array?
        p = pi @ M

        new_name = generate_next_name(pi.name)

        p_new = ProbabilityDistribution(new_name, dtmc, p) 
        # TODO: name is dependent on the previos step, ex. pi = p1 -> p_new = p2

        self.probability_distributions.append(p_new)
    
    '''Task 11. Implement functions that, given a DTMC and an initial probability distribution,
    calculate the probability distribution and the sojourn times in each state after a
    mission of n steps.'''

    def sojournTimes(dtmc, p0, n):
        '''
        DTMC: the DTMC
        p0: the initial probability
        n: number of steps
        '''
        # the probaiblity at step k, given M and p0 is 
        M = DTMC.transitionMatrix
        M_ = p0 @ M
        for i in range(n):
            M_ = M_ @ M

        # TODO: sojourn time ?
        return M

    # Task 12
    def timeSeries(self, dtmc, s0, n):
        """Generates a time series from a DTMC.
            dtmc (DTMC): a DTMC
            s0 (string): intial state
            n (int): number of steps
        """
        currentState = s0
        timeSeries = [currentState]
        possibleStates = dtmc.states
        i = 0
        prob = 1
        while i < n:
            for i in range(len(possibleStates)):
                if currentState == possibleStates[i]:
                    probabilities = dtmc.transitions[i]
                    # nextState = np.random.choice(possibleStates)
                    change = np.random.choice(possibleStates, replace=True, p=probabilities)
                    if change == possibleStates[0]:
                       prob = prob * probabilities[0]
                       timeSeries.append(change)
                    elif change == possibleStates[1]:
                        prob = prob * probabilities[1]
                        timeSeries.append(change)
                    else:
                        prob = prob * probabilities[2]
                        timeSeries.append(change)
                    currentState = change
            i += 1
        print("Possible states: " + str(possibleStates))
        print("End state after " + str(n) + " steps: " + currentState)
        print("Probability of the time series: " + str(prob))
        print("Time series: " + str(timeSeries))
        









        
    
