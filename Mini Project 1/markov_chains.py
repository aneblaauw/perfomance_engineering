#A datastructure to encode DTMC (discrete-time Markov chanis)
import re

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
    
    def checkProbabilities(self):
        for transitions in self.transitionMatrix:
            if sum(transitions) > 1.0:
                raise ValueError(f"The sum of the probabilities {transitions} is greater than 1.")
    

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

# Task 9
class checkCorrectness:
    # probabilit

    def validateMarcovChain(self, dtmc, probability_distribution):
      



# Task 10 