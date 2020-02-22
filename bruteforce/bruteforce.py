import itertools as it
import math
import time

class Brute:
    def __init__(self, input, startnode = 0):
        """
        Takes input as 2D list; Outputs OptimalTour, OptimalCost and Time taken
        """
        self.input = input
        self.startnode = startnode
        
    def algo(self):
        start_time = time.time()
        dataset = self.input
        l= len(dataset)
        for i in list(range(0,l)):
            for j in list(range(0,l)):
                if dataset[i][j] == 0 or dataset[i][j]==-1:
                    dataset[i][j] = math.inf # To avoid going to unconnected nodes
                    
        perm = list(range(1,(l+1)))
        perm = list(it.permutations(perm)) # Permutations
        
        distance = 0
        i = 0
        mindist = math.inf
        for selection in perm:
            start = selection[0]-1
            i = 0
            while i < (l-1):
                new = selection[i+1] - 1
                distance = distance + dataset[start][new]
                start = new
                i = i+1
            new = selection[0]-1
            start = selection[l-1]-1
            distance = distance + dataset[start][new]
            if distance < mindist:
                mindist = distance
                OptimalTour = selection
            distance = 0
            
        OptimalTour = list(OptimalTour)
        
        if OptimalTour[0] != 1:
            for i in list(range(0,l)):
                if OptimalTour[i] == 1:
                    j = i
            List1 = OptimalTour[0:j]
            List2 = OptimalTour[j:l]
            OptimalTour = List2 + List1
        
        OptimalTour.append(1)
        end_time = time.time()
        
        return mindist, OptimalTour, (end_time-start_time)
