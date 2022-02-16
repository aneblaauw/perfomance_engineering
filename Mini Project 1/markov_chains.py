#A datastructure to encode DTMC (discrete-time Markov chanis)



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
        
        




