from models import Token, DTMC, ProbabilityDistribution
import re
import numpy as np


# Task 7
def tokenizeFile(filename):

    tokens = []
    sourceName = filename 
    input = open(sourceName, "r")

    keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'elif', 'await',
    'break', 'class', 'continue', 'of']
    token_specification = [
        ('Number',      r'\d+(\.\d*)?'),  # Integer or decimal number
        ('Delimiters',  r'[;:]'),         # Statement terminator
        ('Identifiers', r'[A-Za-z]+'),    # Identifiers
        ('Operators',   r'[+\-*<>/]'),    # Arithmetic operators
        ('NEWLINE',     r'[\n]+'),        # Line endings
        ('SKIP',        r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',    r'.'),            # Any other character
        
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 0
    for line in input:
        line_num += 1
        line_start = 0
        for mo in re.finditer(tok_regex, line):
            type = mo.lastgroup
            string = mo.group()
            column = mo.start() - line_start
            if type == 'Number':
                string = float(string) if '.' in string else int(string)
            elif type == 'Identifiers' and string in keywords:
                type = 'Keyword'
            elif type == 'Identifiers':
                type = 'Identifiers'
            elif type == 'NEWLINE':
                line_start = mo.end()
                continue
            elif type == 'SKIP':
                continue
            elif type == 'MISMATCH':
                print("error")
            
            tokens.append(Token(type, string, line_num, column))
    
    return tokens

# Task 8
def generateDTMCfromTokens(tokens):
        # generate DTMC and probabilities from a list of token
        # assuming the tokens are sorted after line and column
      
        transitionMatrix = []
        transition = False
        transitions = {}
        states = []
        name = None
        state_f = None # the start state in a transition
        state_t = None # the end state in a transition
        transition_val = None # the transition value for the current transition

        for token in tokens:
            '''
            What we know:
            * the column number depends on the length of the words before, ex
                    CALM -> ROUGH: 0.0;
	                MODERATE -> CALM: 0.6;
                only the first token from these two lines have the same column number
            
            * We can find every token that is on the same line
            * We are only dealing with DTMC and probability distributions, and we can assume that the tokens belong togehter
            (the DTMC belongs to the probability dists)
            * Every object from the tokens ends with an 'end' token
            * Every line ends with an ;
            * The name is the first token in every group of tokens sent in

            '''
            if name == None:
                # we now the current token is the name
                name = token.string
            

            elif token.column == 1:
                transition = True
                # now we know that we are dealing with a transition 
                state_f = token.string
                if not state_f in states:
                    states.append(token.string)

            elif transition:
                if token.type == 'Identifiers':
                    state_t = token.string # the end state in the transition
                    if not state_t in states:
                        states.append(token.string)
                if token.type == 'Number':
                    transition_val = token.string
                if token.string == ';':
                    # end of the transition
                    transition = False
                    transitions[(state_f, state_t)] = transition_val
                
            elif token.string == 'end':
                # finished with the markov Chain, ready to make the DTMC
                # We have the name and the states, need to make the transition matrix
                transitionMatrix = np.zeros((len(states), len(states)))

                for key, value in transitions.items():
                    # the index in the transistion matrix can be found by the key tuple
                    state_from = key[0]
                    state_to = key[1]
                    # finding the indexes in the transition matrix
                    i = states.index(state_from)
                    j = states.index(state_to)
                    transitionMatrix[i][j] = value
                return DTMC(name=name, states=states, transitions=transitionMatrix)
                    


# Task 8
def generateProbDistFromTokens(markov_chain, tokens):
    '''
    Need the MarkovChain to find the belonging DTMC
    probabilities = [1.0, 0.0, 0.0] # one probability for each state
    '''
    # a probability distribution has a name (p0), and a belongning DTMC (identified from name)
        # this is given in the first line
    # Then, for each state in its belonging DTMC, it has a probability
    # Note, the order of the probability list should correspond with the order of the DTMC states

    name = None
    DTMC = None
    probability = False
    probability_list = []
    DTMC = None
    index = None # index for the probability
    for token in tokens:
        if not probability and token.string != 'end':
            if name == None:
                name = token.string
            elif token.type == 'Number':
                # the name consists of a number as well
                name = name + str(token.string)
            elif DTMC == None and token.type == 'Identifiers':
                DTMC_name = token.string
                for dtmc in markov_chain.DTMC_list:
                    if dtmc.name == token.string:
                        DTMC = dtmc
                if DTMC == None:
                    raise ValueError(f'The DTMC %s does not exist' % DTMC_name)
                probability_list = np.zeros(len(DTMC.states))
            
            if token.column == 1:
                probability = True
       
        if probability:
            if token.type == 'Identifiers':
                # can find the index for the probability
                try:
                    index = DTMC.states.index(token.string)

                except:
                    raise IndexError(f"The DTMC %s doesn't have the state %s", DTMC, token.string)
            
            if token.type == 'Number':
                probability_list[index] = token.string
            
            if token.string == ';':
                # probability is finished 
                probability = False
        if token.string == 'end':
            # the tokens are finished, ready to make the probability distribution
            return ProbabilityDistribution(name=name, DTMC=DTMC, probabilities=probability_list)


def generate_next_name(name):
    chars = list(name)
    number = ''
    name = ''
    for char in chars:
        if char.isnumeric():
            number = number + char
        else:
            name = name + char


    new_number = int(number) + 1
    return name + str(new_number)