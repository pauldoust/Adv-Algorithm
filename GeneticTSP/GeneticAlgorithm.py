import math
import random
import numpy as np
import time
          
CHROMOSOME_LENGTH = 0
DISTANCES = []

POPULATION_SIZE = 10
GENERATION_NUM = 10

class Gene:
   def __init__(self, geneName = None, id = 0):
      self.geneName = geneName
      self.geneId = id

   def __getitem__(self, index):
    return self.geneId

   # def __setitem__(self, value):
   #  self.geneId = value

   def getGeneName(self):
      return self.geneName
 
   def getGeneId(self):
      return self.geneId    

   
   def __repr__(self):
      name = self.getGeneName()
      id = self.getGeneId() + 1
      return name


class Individual:
    def __init__(self, genes =[]):
        self.chromosomeGenes = genes
        self.fitness = 0
        # print("const, len: ",len(self.chromosomeGenes))
        if len(self.chromosomeGenes) == 0  :
            for i in range (0, CHROMOSOME_LENGTH):
                self.chromosomeGenes.append(None)

    def __len__(self):
        return len(self.chromosomeGenes)

    def __repr__(self):
        firstCityIndex =0
        # firstHalf = []
        # secondHalf = []
        for i in range(0, len(self.chromosomeGenes)):
            # print(type(self.chromosomeGenes[i]))
            if (self.chromosomeGenes[i].geneId == 0):
                firstCityIndex = i 
                break
        firstHalf = self.chromosomeGenes[0:firstCityIndex]
        secondHalf = self.chromosomeGenes[firstCityIndex:]
        # print("first: ", firstHalf)
        # print("second", secondHalf)
        finalList = []
        finalList.extend(secondHalf)
        finalList.extend(firstHalf)
        # print("Final List:", finalList)
        return str(finalList)

    def __getitem__(self, index):
      return self.chromosomeGenes[index]
   
    def __setitem__(self, key, value):
      self.chromosomeGenes[key] = value

    def setGeneAtIndex(self, gene , index):
        self.chromosomeGenes[index] = gene

    def getGeneAtIndex(self, index):
        return self.chromosomeGenes[index]

    def getChromosomeLength(self):
        return len(self.chromosomeGenes)

    def getFitness(self):
        initialFitness = 0
        for i in range (0, CHROMOSOME_LENGTH):
            if i == CHROMOSOME_LENGTH -1:
                break
            else:
                firstGene = self.chromosomeGenes[i]
                seconGene = self.chromosomeGenes[i+1]
                initialFitness += DISTANCES[firstGene.getGeneId()] [seconGene.getGeneId()]
        initialFitness += DISTANCES[self.chromosomeGenes[-1].getGeneId()] [self.chromosomeGenes[0].getGeneId()]

        return initialFitness


class Population:
    def __init__(self, individuals =[], populationSize = 10):
        self.individuals = individuals
        self.populationSize = populationSize
        if len(self.individuals) == POPULATION_SIZE:
            return
        for i in range(0, populationSize):
            # print(i)
            self.individuals.append(None)


    def getFittest(self):
        fittest = self.individuals[0]
        # print("first: ", fittest.getFitness)
        for i in range(0, self.populationSize):
            if fittest.getFitness() > self.individuals[i].getFitness():
                fittest = self.individuals[i]
        return fittest

    def getFitness(self):
        fitness = 0
        for i in range(0, len(self.individuals)):   
            ithIndividual = self.individuals[i]
            if(ithIndividual is not None):
                fitness += ithIndividual.getFitness()
        return fitness
    def getIndividualAtIndex(self, index):
        return self.individuals[index]


    def setIndividualAtIndex(self, individual, index = None):
        if index is None:
            self.individuals.append(individual)
        else:
            self.individuals[index] = individual



class Universe:
    def __init__(self, mutationRate = 0.5, elitism = True):
        self.mutationRate = mutationRate
        self.elitism = elitism
    
    def crossover(self, father, mother, mid = None):
        child = Individual(genes = [])
        midIndex = int(random.random() * father.getChromosomeLength())
        if mid is not None:
            midIndex = mid
        # print("mid: ", midIndex)
        # print("father: ", father)
        # print("mother: ", mother)

        addedGenes = []
        # print("initial: ", child)
        for i in range(0, midIndex):
            # print("from Father: ", i)
            child.setGeneAtIndex(father.getGeneAtIndex(i), i )
            addedGenes.append(father.getGeneAtIndex(i).getGeneId())
        # print("child from father: ", child)

        if len(addedGenes) == CHROMOSOME_LENGTH:
            # print("final child all from father ", child)
            return child

        index = 0
        for i in range(0, mother.getChromosomeLength()):
            candidate = mother.getGeneAtIndex(i)
            if candidate.getGeneId() not in  addedGenes:
                child.setGeneAtIndex(candidate, midIndex + index )
                addedGenes.append(candidate.getGeneId())
                index = index + 1


        child = self.mutate(child)
        # print("final child: ", child)
        return child

    def mutate(self, individual):
        for i in range(0, individual.getChromosomeLength()):
            if random.random() < self.mutationRate:
                j = int(individual.getChromosomeLength() * random.random())

                firstMutatedGene = individual.getGeneAtIndex(i)
                secondMutatedGene = individual.getGeneAtIndex(j)
                individual.setGeneAtIndex(firstMutatedGene, j)
                individual.setGeneAtIndex(secondMutatedGene, i)
        return individual

    
    def rouletteSelction (self,  currentPoplulation, elitedIndividuals = [] ):

        universalFitness = currentPoplulation.getFitness()
        selectedIndividualForNexGeneration = currentPoplulation.getFittest()
        currentProportionalProbability = 0
        spinRouletteProbability = random.random()
        for i in range (0, currentPoplulation.populationSize):
            ithIndividual = currentPoplulation.getIndividualAtIndex(i)
            currentProportionalProbability += ithIndividual.getFitness() / universalFitness
            if (currentProportionalProbability > spinRouletteProbability):
                selectedIndividualForNexGeneration = ithIndividual
                break

        return selectedIndividualForNexGeneration



    def selection(self, currentPoplulation , type = "ROULETTE_WHEEL", elitedIndividuals = [] ):
        # print("currentPoplulation: " , currentPoplulation)
        return self.rouletteSelction(currentPoplulation = currentPoplulation, elitedIndividuals = [])

    def breed(self, currentPoplulation):
        nexGeneration = Population(populationSize = currentPoplulation.populationSize)
        elitedIndividual = currentPoplulation.getFittest()
        elitedIndividuals = [elitedIndividual]
        nexGeneration.setIndividualAtIndex(elitedIndividual, 0)
        nextGenerationSize = 1
        while nextGenerationSize < currentPoplulation.populationSize:
            fatherToMate = self.selection(currentPoplulation, elitedIndividuals)
            motherToMate = self.selection(currentPoplulation, elitedIndividuals)

            # print("current Pop: ", currentPoplulation.individuals)
            # print("fatherToMate: ", fatherToMate)
            # print("motherToMate: ", motherToMate)
            child = self.crossover(fatherToMate, motherToMate)
            # print("child: ", child)
            nexGeneration.setIndividualAtIndex(child, nextGenerationSize)
            nextGenerationSize += 1

        return nexGeneration



class Genetic:
    def __init__(self, matrix, population_size = 10, generation_number = 10):
        """
        Takes cost matrix as a list and starts journey from 1st node.
        """
        self.matrix = matrix
        self.population_size = population_size
        self.generation_number = generation_number


    def main(self):
        start_time = time.time()
        cities =[]
        global DISTANCES
        global CHROMOSOME_LENGTH
        DISTANCES = self.matrix
        CHROMOSOME_LENGTH = len(self.matrix)
        POPULATION_SIZE = self.population_size
        GENERATION_NUM = self.generation_number
        self.matrix = np.array(self.matrix)
        for i in range (0, self.matrix.shape[0]):
            city = Gene(str(i + 1), i)
            cities.append(city)
        # print(cities)
        tour1 = Individual(cities)
        initialPopulation = [tour1]
        for i in range(1, POPULATION_SIZE):
            newTour = Individual(cities.copy())
            random.shuffle(newTour)
            initialPopulation.append(newTour)

        # print(initialPopulation)

        pop = Population(initialPopulation, POPULATION_SIZE)
        univ = Universe()
        for i in range(0,GENERATION_NUM):
            # print("Pop: ,", pop.individuals)
            pop = univ.breed(pop)

        fittest = pop.getFittest()
        # print(fittest.chromosomeGenes.index(0))
        elapsedTime = time.time() - start_time

        return fittest.getFitness(), fittest, elapsedTime
        #print("Fittest is : ", fittest, " , With Fitness: ", fittest.getFitness())


'''uncomment the following block for testing'''

'''
DISTANCES =np.array ([ 

                [  0, 633, 257,  91, 412, 150,  80, 134, 259, 505, 353, 324,  70, 211, 268, 246, 121],
                [633,   0, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
                [257, 390,   0, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142,],
                [ 91, 661, 228,   0, 383, 120,  77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
                [412, 227, 169, 383,   0, 267, 351, 309, 338, 196,  61, 421, 346, 243, 199, 528, 297],
                [150, 488, 112, 120, 267,   0,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
                [ 80, 572, 196,  77, 351,  63,   0,  29, 232, 444, 292, 297,  47, 150, 207, 332,  29],
                [134, 530, 154, 105, 309,  34,  29,   0, 249, 402, 250, 314,  68, 108, 165, 349,  36],
                [259, 555, 372, 175, 338, 264, 232, 249,   0, 495, 352,  95, 189, 326, 383, 202, 236],
                [505, 289, 262, 476, 196, 360, 444, 402, 495,   0, 154, 578, 439, 336, 240, 685, 390],
                [353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   0, 435, 287, 184, 140, 542, 238],
                [324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   0, 254, 391, 448, 157, 301],
                [ 70, 567, 191,  27, 346,  83,  47,  68, 189, 439, 287, 254,   0, 145, 202, 289,  55],
                [211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   0,  57, 426,  96],
                [268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   0, 483, 153],
                [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   0, 336],
                [121, 518, 142, 84, 297,  35,  29,  36, 236, 390, 238, 301,  55,  96, 153, 336 ,  0 ]
     
                ])


ga = Genetic(DISTANCES)

print(ga.main())
'''
