#A datastructure to encode DTMC (discrete-time Markov chanis)
import re
import numpy as np
from typing import NamedTuple

# Task 1
# a class for encoding a DTMC from a .txt file
class DTMC(object):
    def __init__(self, name, states, transitions):
        # Task 9, checking input
        assert len(transitions) == len(states) 
        for trans in transitions:
            assert len(trans) == len(states), f'The length of the transition %s must be of size %s ' % (trans, len(states))
            assert round(sum(trans)) <= 1.0, f'The sum of the transition %s is greater than 1, sum: %s' % (trans, sum(trans))
        self.name = name
        self.states = states
        self.transitions =  transitions

    def __str__(self):
        return f'DTMC(name=%s)' % self.name
    
    def printTransitions(self):
        for transition in self.transitions:
            print(transition)
    

# Task 2
class ProbabilityDistribution(object):
    def __init__(self, name, DTMC, probabilities):
        # Task 9
        assert len(probabilities) == len(DTMC.states), f'The size of the probabilities %s must be the same as the number of states in %s' % (probabilities, DTMC.states)
        self.name = name
        self.DTMC = DTMC
        self.probabilities = probabilities
    
    def __str__(self):
        return f'ProbabilityDistribution(name=%s, DTMC=%s, probabilities=%s)' % (self.name, self.DTMC.name, self.probabilities)
    

# Task 6
class Token(NamedTuple):
    type: str
    string: str
    line_num: int
    column: int

