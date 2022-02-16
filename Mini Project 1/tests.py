# TEsting markovik Chains
# Task 4

# The states
states = ['CALM', 'MODERATE', 'ROUGH']

# possible sequences of events

transistionName = [['CC', 'CM', 'CR'],  # CALM
                    ['MC', 'MM', 'MR'], # MODERATE
                    ['RC', 'RM', 'RR']] # ROUGH

        
# Probabilities matrix (transition matrix)
transitionMatrix = [[0.6, 0.4, 0.0], # CALM
                    [0.6, 0.3, 0.1], # MODERATE
                    [0.0, 0.9, 0.1]] # ROUGH

probabilities = [1.0, 0.0, 0.0] # one probability for each state

from markov_chains import *

seaCondition = DTMC('SeaCondition', states, transitionMatrix)
p0 = probability_distribution('p0', seaCondition, probabilities)
p1 = probability_distribution('p1', seaCondition, probabilities)

test = MarkovChain(seaCondition, p0, p1)

test.print()
