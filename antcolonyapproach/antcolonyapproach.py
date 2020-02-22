### Robin Khatri
### MLDM M1
### Advanced algorithm TSP project

import random
import time

class AntApproach:
    def __init__(self, input, iterations=100, ants=10):
        """
        Input is a 2-D list which contains cost of travel
        iterations define number of iterations. For most part 100 iterations work very well.
        40 is the number of ants. Should be closer to the number of cities. We chose in [10,50]
        """
        self.dataset = input
        self.iterations=iterations
        self.ants = ants
        
    def Algo(self):
        starttime = time.time()
        dataset = self.dataset    
        l = len(dataset)
        """
        We'll use inf to denote unconnected cities. Since, in TSPLIB (which we used for benchmarking had different 
        values denoting unconnectivity - 9999999, 0, 100000000, -1), we'll replace all these values with inf. These values 
        have to be modified if new value for denoting unonnected cities is encountered. These values work fine for the 
        TSPLIB problems we tested.
        """
        for i in list(range(0,l)):
            for j in list(range(0,l)):
                if dataset[i][j]==0 or dataset[i][j]==-1 or dataset[i][j]==9999999 or dataset[i][j]==100000000:
                    dataset[i][j] = float('inf')
                    
        antcolonyobject = antcolony(self.ants, self.iterations, alpha=1.0, beta=10.0, rho=0.5, q=10)
        """
        alpha controls influence of pheromones in a tansition
        beta controls the desirability of a transition
        rho is evaporation rate, controls how pheromones vanish. It lies in [0,1]
        q is a constant.
        """
        combine = Combine(dataset, l) # To present length and cost matrix
        OptimalTour, mindist = antcolonyobject.solve(combine)
        OptimalTour = [x+1 for x in OptimalTour]
        
        OptimalTour = list(OptimalTour)
        
        if OptimalTour[0] != 1:
            for i in list(range(0,l)):
                if OptimalTour[i] == 1:
                    j = i
            List1 = OptimalTour[0:j]
            List2 = OptimalTour[j:l]
            OptimalTour = List2 + List1
        
        OptimalTour.append(1)
        return mindist, OptimalTour, (time.time()-starttime)
        
class Combine(object):
    def __init__(self, cost_matrix: list, size: int):
        self.matrix = cost_matrix
        self.size = size
        self.pheromone = [[1 / (size * size) for j in range(size)] for i in range(size)] # Pheromone, will be updated et every iteration


class antcolony(object):
    def __init__(self, ant_count: int, iterations: int, alpha: float, beta: float, rho: float, q: int):
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.iterations = iterations
        
    def pheromoneupdate(self, combine: Combine, ants: list):
        for i, row in enumerate(combine.pheromone):
            for j, col in enumerate(row):
                combine.pheromone[i][j] *= self.rho
                for ant in ants:
                    combine.pheromone[i][j] += ant.pheromone_delta[i][j]


    def solve(self, combine: Combine):
        best_cost = float('inf')
        best_solution = []
        for gen in range(self.iterations):
            ants = [_Ant(self, combine) for i in range(self.ant_count)]
            for ant in ants:
                for i in range(combine.size - 1):
                    ant.nextvisit()
                ant.total_cost += combine.matrix[ant.tour[-1]][ant.tour[0]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tour
                # update pheromone
                ant.pheromoneupdate_delta()
            self.pheromoneupdate(combine, ants)
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, antcolonyobject: antcolony, combine: Combine):
        self.colony = antcolonyobject
        self.combine = combine
        self.total_cost = 0.0
        self.tour = []  # tour list
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(combine.size)]  # cities which are allowed for the next visit
        self.eta = [[0 if i == j else 1 / combine.matrix[i][j] for j in range(combine.size)] for i in
                    range(combine.size)]  # Desirability
        start = random.randint(0, combine.size - 1)  # start from any city
        self.tour.append(start)
        self.current = start
        self.allowed.remove(start)

    def nextvisit(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.combine.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                                                                                            i] ** self.colony.beta
        probabilities = [0 for i in range(self.combine.size)]  # probabilities for moving to a city in the next step
        for i in range(self.combine.size):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = (self.combine.pheromone[self.current][i] ** self.colony.alpha) * (self.eta[self.current][i] ** self.colony.beta) / denominator
            except ValueError or ZeroDivisionError:
                pass  
        # select next city randomly with probability - list probabilities
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.tour.append(selected)
        self.total_cost += self.combine.matrix[self.current][selected]
        self.current = selected

    def pheromoneupdate_delta(self):
        self.pheromone_delta = [[0 for j in range(self.combine.size)] for i in range(self.combine.size)]
        for _ in range(1, len(self.tour)):
            i = self.tour[_ - 1]
            j = self.tour[_]
            self.pheromone_delta[i][j] = self.colony.Q / self.total_cost
