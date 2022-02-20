#A datastructure to encode DTMC (discrete-time Markov chanis)
import re
import numpy as np

# Task 1
# a class for encoding a DTMC from a .txt file
class DTMC:
    def __init__(self, name, states, transitions):
        self.name = name
        self.states= states
        #self.transitionName = [] #TODO: implement transition names?
        self.transitionMatrix = transitions
    
    def __str__(self):
        return self.name


    # Task 9, check that no transition is greater than 1
    def checkProbabilities(self):
        for transitions in self.transitionMatrix:
            if sum(transitions) > 1.0:
                raise ValueError(f"The sum of the probabilities {transitions} is greater than 1.")
    
    # Asummes that 'without in and out transitions' means that every transition must be present
    def checkTransitions(self):
        # the size of the tranision matrix must be of nxn when it has n number of states
        if len(self.transitionMatrix) != len(self.states) or len(self.transitionMatrix[0]) != len(self.states):
            raise ValueError(f"The DTMC are missing transitions")
    
    # TODO: implement check before creating the object 

    

# Task 2
class probability_distribution:

    def __init__(self, name, DTMC, probabilities):
        self.name = name
        self.DTMC = DTMC
        self.probabilities = probabilities # The length of the probabilities must be equal to the number of states the DTMC has

    def __str__(self):
        return self.name
    
    def setProbabilities(self, probabilities):
        self.probabilities = probabilities
    
    def getProbabilities(self):
        return self.probabilities
    


# Task 3
class MarkovChain:
    # assuming you want to manage one DTMC with an unknown number of probability distributions
    def __init__(self, DTMC, *probability_distributions):
        self.DTMC = DTMC
        self.probability_distributions = list(probability_distributions)

    # Task 5
    def print(self, filename=None):
        if filename is None:
            filename = str(self.DTMC) + ".txt"
        path = 'textFiles/'
        f = open(path + filename, 'w')
        
        f.write('MarkovChain ' + str(self.DTMC)+ "\n") # TODO: make DTMC return name as __str__()
        # writing the states
        for i in range(len(self.DTMC.states)):
            for j in range(len(self.DTMC.states)):
                f.write("\t" + self.DTMC.states[i] + " -> " + self.DTMC.states[j]+": " + str(self.DTMC.transitionMatrix[i][j]) + ";\n")
        
        f.write("end \n \n")

        # writing the probability distributions
        for dist in self.probability_distributions:
            f.write('ProbobailityDistribution ' + str(dist) + " of " + str(dist.DTMC) + '\n')
            for i in range(len(dist.probabilities)):
                f.write('\t' + dist.DTMC.states[i] + ': ' + str(dist.probabilities[i]) + ';\n')
            f.write('end \n \n')
        f.close

    def generateDTMCfromToken(tokens):
        # generate DTMC and probabilities from a list of token
        # assuming the tokens are sorted after line and column

        # TODO: add name to tokens
        name = ''
        states = []
        transitionMatrix = []
        # Probabilities matrix (transition matrix)
        transitionMatrixEx = [[0.6, 0.4, 0.0], # CALM
                        [0.6, 0.3, 0.1], # MODERATE
                        [0.0, 0.9, 0.1]] # ROUGH
        # The states
        statesEx = ['CALM', 'MODERATE', 'ROUGH']

        lines = []


        for token in tokens:
            if not token.line_num in lines:
                lines.append(token.line_num)

            if token.type == 'Identifiers':
                if not token.string in states:
                    states.append(token.string)
        print(states)
        transitionMatrix = np.zeros((len(states), len(states)))

        for token in tokens:
            pass

        print(transitionMatrix)

    # Task 10
    # Assuming the task is to calculate the next step
    def computeNextStep(self, pi):
        M = self.DTMC.transitionMatrix #numpy array?
        p = pi @ M

        p_new = probability_distribution('p_2', self.DTMC, p) 
        # TODO: name is dependent on the previos step, ex. pi = p1 -> p_new = p2

        self.probability_distributions.append(p_new)
    
    '''Task 11. Implement functions that, given a DTMC and an initial probability distribution,
    calculate the probability distribution and the sojourn times in each state after a
    mission of n steps.'''

    def sojournTimes(DTMC, p0, n):
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




# Task 6

class Token:

    def __init__(self, type, string, line, column):  
        self.type = type
        self.string = string
        self.line = line
        self.column = column

    def setType(self, type):
        self.type = type
    
    def getType(self):
        return self.type

    def setString(self, string):
        self.string = string  
          
    def getString(self):
        return self.string
     
    def setLine(self, line):
        self.line = line

    def getLine(self):
        return self.line
   
    def setColumn(self, column):
        self.column = column
    
    def getColumn(self):
        return self.column
  

class tokenize:
    # Task 7 - må bruke Token classen på en måte
    def readFileToTokens(self, file):
        
        sourceName = file 
        input = open(sourceName, "r")

        tokens = []
        for line in input:
            line = line.rstrip()
            newLine = re.sub(r"#.*", r"", line)  # Sletter alle kommentarer
            while newLine!="": # if the new line is different from an empty line
                if re.match(r"^[ \t]+", newLine): # want to match anything but the whitespace and the tabular
                    newLine = re.sub(r"^[ \t]+", "", newLine) # substitute whitespace and tab by nothing
                elif re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", newLine): # New line start with an identifier
                    identifier = re.match(r"[a-zA-Z_][a-zA-Z0-9_]*", newLine).group()
                    newLine = re.sub(r"^[a-zA-Z_][a-zA-Z0-9_]*", "", newLine) # Remove the identifier from Newline
                    # type = 'identifier'
                    tokens.append(identifier)
                elif re.match(r'"[^"]*"', newLine): # Regular expression for stings 
                    string = re.match(r'"[^"]*"', newLine).group()
                    newLine = re.sub(r'"[^"]*"', "", newLine)
                    tokens.append(string)
                else:
                    character = newLine[0] # Pick up the first character of the line
                    newLine = newLine[1:]
                    tokens.append(character)

        input.close()




    
# Task 10

