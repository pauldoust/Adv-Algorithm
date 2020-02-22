import numpy as np
import heapq
import copy
import time

INFINITY = np.inf


# DISTANCES = [ 
#                [INFINITY, 3, 93, 13, 33, 9, 57],
#                [4, INFINITY, 77, 42, 21, 16, 34],
#                [45, 17, INFINITY, 36, 16, 28, 25],
#                [39, 90, 80, INFINITY, 56, 7, 91],
#                [28, 46, 88, 33, INFINITY, 25, 57],
#                [3, 88, 18, 46, 92, INFINITY, 7],
#                [44, 26, 33, 27, 84, 39, INFINITY]
#             ]

class AddRemoveEdges:

    def __init__(self, matrix):
        self.matrix = matrix
        self.upperBound = np.inf
        self.bestSol = []

    def reduceMatrix(self, matrix, lowerBound):
        rows = matrix.shape[0]
        cols = matrix.shape[1]
        if(rows ==  0 or cols == 0):
            return matrix, lowerBound

        rowsMin = np.nanmin(matrix,axis =1)
        where_are_NaNs = np.isnan(rowsMin)
        where_are_Inf = np.isinf(rowsMin)
        rowsMin[where_are_NaNs] = 0
        rowsMin[where_are_Inf] = 0
        rowsMin = rowsMin.reshape(rows,1)

        matrix = matrix  - rowsMin

        colsMin = np.nanmin(matrix, axis = 0)
        where_are_NaNs = np.isnan(colsMin)
        where_are_Inf = np.isinf(colsMin)
        colsMin[where_are_NaNs] = 0
        colsMin[where_are_Inf] = 0
        colsMin = colsMin.reshape(1,cols)


        matrix = matrix - colsMin

        lowerBound = lowerBound +  np.sum(rowsMin) + np.sum(colsMin)

        return matrix,lowerBound


    def chooseSplittingEdge(self, matrix):
        rows = matrix.shape[0]
        cols = matrix.shape[1]

        splittingCandidateRow = -1
        splittingCandidateCol = -1

        maximumLowerBound = - np.inf
        smallestInRow = np.inf
        smallestInCol = np.inf
        for i in range(0, rows):
            for j in range(0, cols):
                if matrix[i][j] == 0:
                    matrix [i][j] = -1
                    rowMinCandidates = [x for x in matrix[i,:] if ( x >= 0)]
                    colMinCandidates = [x for x in matrix[:, j] if x >= 0]
                    if rowMinCandidates != []:
                        smallestInRow = min( rowMinCandidates)
                    if colMinCandidates !=[]:
                        smallestInCol = min(colMinCandidates)
                    matrix[i][j] = 0

                    if smallestInCol + smallestInRow > maximumLowerBound:
                        maximumLowerBound = smallestInRow + smallestInCol
                        splittingCandidateCol = j
                        splittingCandidateRow = i

        return splittingCandidateRow, splittingCandidateCol



    def excludeEdge(self, matrix, i, j,lowerBound):
        matrix[i,j] = INFINITY
        matrix, lowerBound = self.reduceMatrix(matrix, lowerBound)
        return matrix, lowerBound

    def edges_to_node(self, solution):
        current_vertex = "1"
        node_list = []
        edges = copy.deepcopy(solution)
        while len(edges) > 0:
            for pair in edges:
                nodes = pair.split(",")
                if nodes[0] == current_vertex:
                    node_list.append(current_vertex)
                    current_vertex = nodes[1]
                    edges.remove(pair)
        node_list.append("1")
        return node_list

    def includeEdge(self, matrix, i,j, lowerBound, solution):

        if (np.isnan (matrix[j,i])) == False:
            matrix[j,i] = INFINITY
        # matrix[j,i] = INFINITY
        matrix[i,:] = np.full((1,matrix.shape[1]), np.nan)
        matrix[:,j] = np.full((1,matrix.shape[0]), np.nan)



        matrix, lowerBound = self.reduceMatrix(matrix, lowerBound)

        sol = solution.copy()
        edgeToPrint = str(i+1) + "," + str(j+1)

        sol.append(edgeToPrint)
        if len(sol) != matrix.shape[0] -1:
            subpathes=[]
            for edge in sol:
                source = edge.split(",")[0]
                target = edge.split(",")[1]
                subpath=[]
                subpath.append(edge)
                noMore = True
                newTraget = target
                while noMore:      
                    # print("Stuck Here", matrix.shape[0])
                    # print("Stuck Here", sol)
                    # matching = [s for s in sol if str('\'',newTraget+',') in s]
                    matching = [s for s in sol if newTraget == s.split(",")[0]]
                    # matching
                    if len(matching) == 0:
                        noMore = False
                        break
                    subpath.extend(matching)
                    newTraget = matching[0]
                    newTraget = newTraget.split(",")[1]
                    if newTraget == target:
                        noMore =False


                lastEdge  = subpath[-1]
                firstEdge = subpath[0]
                lastNode = lastEdge.split(",")[1]
                firstNode = firstEdge.split(",")[0]
                lastNode = int(lastNode)
                firstNode = int(firstNode)
                lastNode = lastNode -1
                firstNode = firstNode -1
                if (np.isnan(matrix[lastNode, firstNode]) == False):
                 matrix[lastNode, firstNode] = INFINITY


        return matrix, lowerBound


    def isValidSolution (self, matrix, solution):
        if len(solution) == matrix.shape[0]:
            return True

        return False

        # if len(solution) < matrix.shape[0]:
        #     return False

        # return True

        partialSolution = np.full((1, matrix.shape[0]), -1)
        partialSolution = partialSolution[0]
        for edge in solution:
            source = edge.split(",")[0]
            target = edge.split(",")[1]
            source = int(source)
            target = int(target)
            source = source -1
            target = target -1
            partialSolution[source] = target

        first = 0
        last = partialSolution[0]
        visitedNodes = np.full((1, matrix.shape[0]), False)
        visitedNodes = visitedNodes[0]
        visitedNodes [first] = True
        while first != last:
            if visitedNodes[last] == True:
                return False
            visitedNodes[last] = True
            last = partialSolution[last]

        if all(visitedNodes.tolist()):
            return True

        return False

    def branchAndBound(self, matrix, lowerBound, solution,  depth, name = "root"):
        # print("----------------------")
        # print(name)
        # print("depth: ", depth)
        # print('initial lowerBound: ', lowerBound)
        # print('current upperBound: ', self.upperBound)
        # print('\nCurrentMatrix:\n ', matrix)

        if lowerBound > self.upperBound:
            # print ("lower bound is : ",lowerBound, "and higher than the found upperBound: ",self.upperBound, " prunned")
            return

        # if depth == matrix.shape[0] :
        if len(solution) == matrix.shape[0] :
            if self.isValidSolution(matrix, solution):
                # print("found solution: ")
                # print(solution)
                # print("cost: ", lowerBound)
                if lowerBound < self.upperBound:
                    self.upperBound = lowerBound
                    self.bestSol = solution.copy()
                return matrix
            else:
                if depth == matrix.shape[0] :
                    # print('no valid solution')
                    return


        i,j = self.chooseSplittingEdge(matrix)
        # print("split on: ", i+1, " ", j+1)
        if  i ==-1 and j==-1 :
            return


        includeEdgeMat,IncludeLowerBound = self.includeEdge(np.copy(matrix), i,j, lowerBound, solution)
        edgeToPrint = str(i+1) + "," + str(j+1)
        edge = str(i) + "," + str(j)
        # print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound," \nMatrix: \n",includeEdgeMat )
        # print("include(",edgeToPrint," )", "\nCost: ", IncludeLowerBound)
        solution.append(edgeToPrint)
        self.branchAndBound(includeEdgeMat, IncludeLowerBound, solution, depth+1, name = "Solution with " + edgeToPrint)
        solution.pop()

        excludeEdgeMat,excludeLowerBound = self.excludeEdge(np.copy(matrix), i, j, lowerBound)
        # print("exclude(",i+1," ",j+1," )",  "\nCost: ", excludeLowerBound)

        self.branchAndBound(excludeEdgeMat, excludeLowerBound, solution, depth+1,name = "Solution without " + edgeToPrint)

    def main(self):
        start_time = time.time()
        x = np.array(self.matrix)
        # print(self.matrix)
        #ensure all the zeros or negative values are set to inifinity,
        #zero has a special meaining for this algorithnm
        x[x <= 0] = np.inf
        lowerBound = 0

        reducedMat,lowerBound = self.reduceMatrix(x,lowerBound)

        print(lowerBound)
        self.branchAndBound(reducedMat, lowerBound,[], 0)
        return self.upperBound, self.edges_to_node(self.bestSol), time.time() - start_time

        #print("Final Solution = ", bestSol)
        #print("Final Cost = ", upperBound)

#main()


''' Uncomment the above code to test  '''

# DISTANCES =  [ 

#                 [  INFINITY, 633, 257,  91, 412, 150,  80, 134, 259, 505, 353, 324,  70, 211, 268, 246, 121],
#                 [633,   INFINITY, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
#                 [257, 390,   INFINITY, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142,],
#                 [ 91, 661, 228,   INFINITY, 383, 120,  77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
#                 [412, 227, 169, 383,   INFINITY, 267, 351, 309, 338, 196,  61, 421, 346, 243, 199, 528, 297],
#                 [150, 488, 112, 120, 267,   INFINITY,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
#                 [ 80, 572, 196,  77, 351,  63,   INFINITY,  29, 232, 444, 292, 297,  47, 150, 207, 332,  29],
#                 [134, 530, 154, 105, 309,  34,  29,   INFINITY, 249, 402, 250, 314,  68, 108, 165, 349,  36],
#                 [259, 555, 372, 175, 338, 264, 232, 249,   INFINITY, 495, 352,  95, 189, 326, 383, 202, 236],
#                 [505, 289, 262, 476, 196, 360, 444, 402, 495,   INFINITY, 154, 578, 439, 336, 240, 685, 390],
#                 [353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   INFINITY, 435, 287, 184, 140, 542, 238],
#                 [324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   INFINITY, 254, 391, 448, 157, 301],
#                 [ 70, 567, 191,  27, 346,  83,  47,  68, 189, 439, 287, 254,   INFINITY, 145, 202, 289,  55],
#                 [211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   INFINITY,  57, 426,  96],
#                 [268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   INFINITY, 483, 153],
#                 [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   INFINITY, 336],
#                 [121, 518, 142, 84, 297,  35,  29,  36, 236, 390, 238, 301,  55,  96, 153, 336 ,  INFINITY ]
     
#                 ]

# DISTANCES = [
#                  [INFINITY, 8, 14, -1, -1, -1, -1, -1, 7, 12, 6, -1, -1, 7, 11, 7],
#                  [8, INFINITY, 14, -1, 10, 9, 5, 11, 13, 13, 10, 11, 13, 6, -1, 8],
#                  [14, 14, INFINITY, 5, 12, -1, -1, 10, 8, -1, 9, 8, 14, 13, 14, 5],
#                  [-1, -1, 5, INFINITY, 10, 13, 11, 6, 9, 8, 14, 5, 12, 7, 13, 7],
#                  [-1, 10, 12, 10, INFINITY, 6, 13, 13, -1, -1, 9, -1, 7, 13, 6, 12], 
#                  [-1, 9, -1, 13, 6, INFINITY, 11, 11, -1, 11, 9, 5, 9, 8, 7, 12],
#                  [-1, 5, -1, 11, 13, 11, INFINITY, 9, 6, 6, 12, 13, 5, 8, -1, 5], 
#                  [-1, 11, 10, 6, 13, 11, 9, INFINITY, 13, -1, 9, 10, 6, 9, -1, 9], 
#                  [7, 13, 8, 9, -1, -1, 6, 13, INFINITY, 13, 11, 5, 14, 11, 6, 11], 
#                  [12, 13, -1, 8, -1, 11, 6, -1, 13, INFINITY, 12, 7, 5, 7, 7, 12], 
#                  [6, 10, 9, 14, 9, 9, 12, 9, 11, 12, INFINITY, 11, 5, 9, 6, 14], 
#                  [-1, 11, 8, 5, -1, 5, 13, 10, 5, 7, 11, INFINITY, 8, 6, 10, 14], 
#                  [-1, 13, 14, 12, 7, 9, 5, 6, 14, 5, 5, 8, INFINITY, 10, 10, 13],
#                  [7, 6, 13, 7, 13, 8, 8, 9, 11, 7, 9, 6, 10, INFINITY, 13, 7],
#                  [11, -1, 14, 13, 6, 7, -1, -1, 6, 7, 6, 10, 10, 13, INFINITY, 8],
#                  [7, 8, 5, 7, 12, 12, 5, 9, 11, 12, 14, 14, 13, 7, 8, INFINITY]
#                  ]


# DISTANCES = [
#               [INFINITY, 92, 832, 269, 57, 283], 
#               [92, INFINITY, 683, 664, 775, 250], 
#               [832, 683, INFINITY, 818, 140, 574], 
#               [269, 664, 818, INFINITY, 835, 316], 
#               [57, 775, 140, 835, INFINITY, 331],
#               [283, 250, 574, 316, 331, INFINITY]
#              ]


# a = AddRemoveEdges(DISTANCES)
# print(a.main())

