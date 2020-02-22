#!/usr/bin/python
""" Dynamic Programming Algorithm

This script solve a TSP problem given a adgency matrix using
Dynamic Programming Algorithm

Author : Laetitia Couge
Master MLDM1
Date : November 2018
"""
import sys
import itertools
import time
from Generator import Generator
#from tslib import tslib
import datetime
import os
import psutil
from sys import getsizeof
import gc


class TspDp( object ):

    def __init__( self, input, start_node=0 ):
        """ class initializer
           parameters :
           ----------
           input: 2D list
           start_node : which node to start the TSP problem
        """
        self._input = input
        self._start_node = start_node
        self._nb_node = len(input[0])
        self._nb_subset = 1<<self._nb_node
        self._all_set = (1<<self._nb_node) - 1
        self.convert_no_link()

    def run(self):
        return self.compute_sub_problems(self._start_node)

    def convert_no_link(self):
        """Change value for non connected nodes from -1 to INF"""
        for i in range(self._nb_node):
            for j in range(self._nb_node):
                if self._input[i][j] == -1:
                    self._input[i][j] = float("inf")


    def print_node_subset(self, subset):
        """print the list of node in the subset"""
        node_list=[]
        k=0
        while subset:
            if subset&1:
                node_list.append(k)
            k=k+1
            subset = subset>>1
        print(node_list)


    def generate_subset_by_size(self, nb_node, subset_size, start_node):
        """ Generate subset of subset_size nodes among nb_node nodes. Without include start node.
        """
        N=[]
        S=[]

        for i in range(nb_node):
            N.append(i)
        N.remove(start_node)
        for subset in (itertools.combinations(N, subset_size)):
            #print(subset)
            value = 0
            for item in subset:
                value = value + (1<<item)
            if value:
                S.append(value)

        return(tuple(S))  #carreful it is because start node is node 0


    def compute_sub_problems(self, start_node):
        """ resolve TSP problem with Dynamic Programming Algorithm
        """
        start_time = time.time()
        nb_subset = pow(2,self._nb_node)

        T=[0]*self._nb_node
        T_first=[0]*self._nb_node
        T=[[float("inf")]*nb_subset for _ in range(0,self._nb_node)]

        P=[0]*self._nb_node
        P=[[None]*nb_subset for _ in range(0,self._nb_node)]

        T = {}
        T_first = {}
        for node in range(0,self._nb_node):
            P[node] = {}
            T[node] = {}
            T[node][(1 << node)] = self._input[node][start_node]


        #print(self.get_size(T_first))
        #process = psutil.Process(os.getpid())

        # compute cost for all the sets of node by increasing size.
        #A set of size N requires cost of sets of size N-1
        for k in range(2,self._nb_node):
            #print(k)
            #print(process.memory_info().rss)
            subset_list = self.generate_subset_by_size(self._nb_node, k, start_node)
            #print("Nb set=",len(subset_list))

            for subset in subset_list:
                #self.print_node_subset(subset)
                for first_node in range(0,self._nb_node):

                    if (first_node!=start_node) and ((subset>>first_node)&1):
                        #print("first_node="+str(first_node))
                        mask = subset^(1<<first_node)

                        if mask:
                            min_cost = float("inf")
                            min_cost_node = -1
                            for next_node in range(0,self._nb_node):
                                if next_node!=start_node and next_node!=first_node and ((subset>>next_node)&1):
                                    #print("Next_node=",next_node,"  mask=",mask,  "   cost=",T[next_node][mask], "   d=",self._input[next_node][first_node])
                                    if (T[next_node][mask]+self._input[first_node][next_node])<min_cost:
                                        min_cost = T[next_node][mask]+self._input[first_node][next_node]
                                        min_cost_node = next_node

                            if first_node not in T_first.keys():
                                T_first[first_node] = {}
                            T_first[first_node][subset] = min_cost
                            P[first_node][subset] = min_cost_node

            #print("***",self.get_size(T))
            self.clear_dictionnary_list(T)
            self.copy_dictionnary_list(T_first,T)
            self.clear_dictionnary_list(T_first)
            gc.collect()
            #print(process.memory_info().rss)

        complete_set=(1<<self._nb_node)-1
        mask=complete_set^(1<<start_node)
        min_cost = float("inf")
        first_node = -1

        for node in range(0,self._nb_node):
            if node!=start_node:
                T[node][complete_set] = T[node][mask]+self._input[start_node][node]
                if min_cost > T[node][complete_set]:
                    min_cost = T[node][complete_set]
                    first_node = node

        P[start_node][complete_set] = first_node

        path=[start_node+1]
        first_node = start_node
        mask=complete_set

        while mask in P[first_node].keys():
            next_node = P[first_node][mask]
            mask=mask^(1<<first_node)
            path.append(next_node+1)
            first_node=next_node

        path.append(self._start_node+1)
        end_time = time.time()
        #print("Optimal Tour:", path, ", Optimal Cost:", int(min_cost), ", time taken:", (end_time-start_time))
        return min_cost, path, (end_time-start_time)

    def clear_dictionnary_list(self,listOfDict):
        """" Delete all dictionary keys in the list of dictionary
        """
        for item in listOfDict.keys():
            listOfDict[item].clear()
        listOfDict.clear()
        listOfDict = {}

    def copy_dictionnary_list(self,sourceDict,destDict):
        """" Copy all dictionnaries in the list of dictionnary
        """
        for key_node in sourceDict.keys():
            destDict[key_node] = {}
            destDict[key_node] = sourceDict[key_node].copy()

    def get_size(self, obj, seen=None):
        """Recursively finds size of objects"""
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        seen.add(obj_id)
        if isinstance(obj, dict):
            size += sum([self.get_size(v, seen) for v in obj.values()])
            size += sum([self.get_size(k, seen) for k in obj.keys()])
        elif hasattr(obj, '__dict__'):
            size += self.get_size(obj.__dict__, seen)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum([self.get_size(i, seen) for i in obj])
        return size


if __name__ == '__main__':
    # Create a new generator.
    generator = Generator()

    #matrix=[[9999,10,15,20],[5,999,9,10],[6,13,999,12],[8,8,9,999]]
    #matrix = generator.read_from_file('test_files/test_matrix25')

    #generator.print_nicely(matrix)

    #tslib_pb = tslib('E:/Dev/MLDMProoject/ALL_tsp/rat99.tsp.gz')
    #tslib_pb = tslib('E:/Dev/MLDMProoject/ALL_tsp/bayg29.tsp.gz')
    #matrix = tslib_pb.get_matrix()
    #print(matrix)
    #print(datetime.datetime.now())
    #tsp_pb = TspDp(matrix)
    #print(datetime.datetime.now())

    # Generate a new matrix with given parameters.
    # for k in range(3,26):
    #     print ("Nb Node=",k)
    #     for sparsity in range(2,k+2):
    #         print("****sparsity=",sparsity,"****")
    #
    #         matrix = generator.generate(k, sparsity, 1, 1000, False)
    #         generator.print_nicely(matrix)
    #          # # Save the matrix locally.
    #         generator.save_to_file(matrix, 'E:\Dev\MLDMProoject\Code\test_files_lib\'+''test_files_lib\stsp_matrix_'+str(k)+'_'+str(sparsity))
    #         generator.print_nicely(matrix)
    # root='E:\\Dev\\MLDMProoject\\Code\\'
    #
    # foutput = open("E:\Dev\MLDMProoject\Code\dynamic_test_result_atsp_sparsity3.txt",'w')
    # for k in range(18,20):
    #     print ("Nb Node=",k)
    #     for sparsity in range(2,k+2):
    #         matrix = generator.read_from_file(root+'test_files_lib/atsp_matrix_'+str(k)+'_'+str(sparsity))
    #         generator.print_nicely(matrix)
    #         tsp_pb = TspDp(matrix)
    #         print(sparsity)
    #         cumul_time = 0
    #         nb_it=1
    #         start_time = time.time()
    #         for it in range(0,nb_it):
    #             cost, path, runtime = tsp_pb.compute_sub_problems(0)
    #             #print(str(cost) + "\t\t" + str(runtime) + "\t" + str(path))
    #         end_time = time.time()
    #         cumul_time = (end_time-start_time)/nb_it
    #         foutput.write(str(k)+"\t"+ str(sparsity)+"\t"+str(cost) + "\t" + str(cumul_time) + "\t" + str(path)+"\n")
    # foutput.close()



# foutput=open("E:\Dev\MLDMProoject\Code\dynamic_test_result_atsp.txt",'w')
# for k in range(3,25):
# print("pb size=",k)
# matrix = generator.read_from_file('test_files_lib/atsp_matrix_'+str(k))
# tsp_pb = TspDp(matrix)
# cost,path, runtime = tsp_pb.compute_sub_problems(0)
# print(str(cost) + "\t\t" + str(runtime) + "\t" + str(path))
# foutput.write(str(cost) + "\t" + str(runtime) + "\t" + str(path)+"\n")

# foutput.close()
