#!/usr/bin/python
""" Randomized Algorithm

This script solve a TSP problem given a adgency matrix using 
Randomized Algorithm

Author : Laetitia Couge
Master MLDM1
Date : November 2018
"""
import time
import sys
import itertools
import math
import random
from Generator import Generator

class TspRandom( object ):
    """ Provide random path for TSP
    """
    def __init__( self, input, start_node=0 ):
        self._input = input
        self._start_node = start_node
        self._nb_node = len(input)
        self._nb_subset = 1<<self._nb_node
        self._all_set = (1<<self._nb_node) - 1

        self._cost = float("inf")
        self._opt_path = []
        self._time = 0
        random.seed()

    def run(self):
        return self.compute_sub_problems(self._start_node)

    def convert_no_link(self):
        for i in range(self._nb_node):
            for j in range(self._nb_node):
                if self._input[i][j] == -1:
                    self._input[i][j] = float("inf")

    def get_next_node(self, search_val, prob, node_order, start, end):

        mid_val = int((start+end)/2)
        ret_value =- 1

        if (end-start) == 1:
            if (search_val<=prob[node_order[start]]):
                ret_value = node_order[start]
            elif (prob[node_order[start]]<search_val) and (prob[node_order[end]]>=search_val):
                ret_value = node_order[end]

        elif (prob[node_order[mid_val]]>search_val):
            ret_value = self.get_next_node(search_val, prob, node_order, start, mid_val)
        elif (prob[node_order[mid_val]]<search_val):
            ret_value= self.get_next_node(search_val, prob, node_order, mid_val, end)
        else:
            ret_value = node_order[mid_val]

        return ret_value


    def compute_sub_problems(self, start_node):
        """ Compute the random path starting with source_node
        """
        start_time = time.time()
        S=[]
        for i in range(self._nb_node):
            S.append(i)
        S.remove(start_node)
        min_cost = float("inf")

        path=[]
        path.append(start_node)

        node_src = start_node
        path_cost=0
        while len(S)>1:
            #print(S)
            proba_cost={}
            total_cost=0
            nb_node = 0
            Sprime = []
            for node in S:
                if node != node_src and self._input[node_src][node] != -1:
                    total_cost = total_cost + self._input[node_src][node]
                    nb_node = nb_node+1
                    Sprime.append(node)
            if nb_node>1:

                norm = total_cost*(nb_node-1)
                for node in Sprime:
                    if node != node_src and self._input[node_src][node]!=0:
                        proba_cost[node]=(total_cost-self._input[node_src][node])/norm
                #print(proba_cost)
                cumul_proba = 0
                node_inc=[]
                for key, value in sorted(proba_cost.items(), key=lambda item: (item[1], item[0])):
                    proba_cost[key] = proba_cost[key] + cumul_proba
                    cumul_proba = proba_cost[key]
                    node_inc.append(key)
                    
                proba_cost[node_inc[-1]] = 1.0
                rand = random.uniform(0, 1)
                next_node = self.get_next_node(rand, proba_cost, node_inc, 0, len(node_inc))
                path_cost = path_cost + self._input[node_src][next_node]
                node_src = next_node
            else:
                if nb_node == 1:
                    next_node = Sprime[0]
                    path_cost = path_cost + self._input[node_src][next_node]
                    node_src = next_node
                else:
                    path_cost=float("inf")
                    break
            if path_cost != float("inf"):
                path.append(node_src)
                S.remove(node_src)


        if path_cost != float("inf"):
            path_cost = path_cost + self._input[path[-1]][S[0]]
            path_cost = path_cost + self._input[S[0]][start_node]
            path.append(S[0])
            path.append(start_node)
            for i in range(0,len(path)):
                path[i] = path[i] + 1

        else:
            path=[]
        self._cost = path_cost
        self._opt_path = path
        self._time = 0

        end_time = time.time()
        #print("Tour:", path, ", Optimal Cost:", int(path_cost), ", time taken:", (end_time-start_time))
        return path_cost, path, (end_time-start_time)

    def get_cost(self):
        return(self._cost)

    def get_opt_path(self):
        return(self._opt_path)

    def run_time_limit_iteration(self, time_limit, start_node):
        elapse_time = 0
        start_time=time.time()
        min_cost = float("inf")
        opt_path=[]
        while (time.time()-start_time)<time_limit:
            self.compute_sub_problems(0)
            cost = tsp_pb.get_cost()
            if cost<min_cost:
                min_cost = cost
                opt_path = self.get_opt_path()

        end_time = time.time()
        return min_cost, opt_path, (end_time-start_time)




if __name__ == '__main__':
    #matrix=[[float("inf"),10,15,20],[5,float("inf"),9,10],[6,13,float("inf"),12],[8,8,9,float("inf")]]
    #print(matrix)

    #
    # Create a new generator.
    generator = Generator()

    # Generate a new matrix with given parameters.
    #matrix = generator.generate(8, 8, 1, 100, True)

    # Save the matrix locally.
    #generator.save_to_file(matrix, 'test_files/test_matrix')

    # Read and print the matrix
    matrix = generator.read_from_file('E:/test_matrix3')
    generator.print_nicely(matrix)
    min_cost = float("inf")
    opt_path=[]
    start_time = time.time()
    tsp_pb = TspRandom(matrix)

    # for k in range(0,100000):
    # tsp_pb.compute_sub_problems(0)
    # cost = tsp_pb.get_cost()
    # if cost<min_cost:
    # min_cost = cost
    # opt_path = tsp_pb.get_opt_path()

    root='E:\\Dev\\MLDMProoject\\Code\\'
    root2='E:\Dev\GitHub\\Algo2\\tsp_project\\data\\'
    foutput = open(root+"random_test_result_stsp_sparsity.txt",'w')
    for k in range(3,26):
        print("Nb Node=",k)
        for sparsity in range(2,k+2):
            print("Sparcity=",sparsity)
            matrix = generator.read_from_file(root2+'stsp_matrix_'+str(k)+'_'+str(sparsity))
            generator.print_nicely(matrix)
            tsp_pb = TspRandom(matrix)
            print(sparsity)
            cumul_time = 0
            nb_it=100
            start_time = time.time()
            min_cost = math.inf
            opt_path = []
            for it in range(0,nb_it):
                cost, path, runtime = tsp_pb.compute_sub_problems(0)
                if cost<min_cost:
                    min_cost = cost
                    opt_path = path
                #print(str(cost) + "\t\t" + str(runtime) + "\t" + str(path))
            end_time = time.time()
            cumul_time = (end_time-start_time)/nb_it
            foutput.write(str(k)+"\t"+ str(sparsity)+"\t"+str(min_cost) + "\t" + str(cumul_time) + "\t" + str(opt_path)+"\n")
    foutput.close()



