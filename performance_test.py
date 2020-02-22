import math
import sys
import copy
import time

from branchandbound.BranchAndBoundTSP import BranchAndBound
from bruteforce.bruteforce import Brute
from dynamic.tspdp import TspDp
from randomTSP.tsprandom import TspRandom
from Greedy.Greedy import GreedyTsp
from GeneticTSP.GeneticAlgorithm import Genetic
from MST.MST import MST
from BnBAddingRemovingEdges.BnB import AddRemoveEdges
from antcolonyapproach.antcolonyapproach import AntApproach
from Generator import Generator
from Parser import Parser

ROOT_PATH_ATSP="E:/Dev/MLDMProoject/ALL_tsp/"

LIST_OF_SYMETRIC_PROBLEM=[
   "a280.tsp",
   "ali535.tsp",
   "att48.tsp",
   "att532.tsp",
   "bayg29.tsp",
   "berlin52.tsp",
   "bier127.tsp",
   "brazil58.tsp",
   # "brd14051.tsp",
   "brg180.tsp",
   "burma14.tsp",
   "ch130.tsp",
   "ch150.tsp",
   "d1291.tsp",
   #"d15112.tsp",
   #"d1655.tsp",
   #"d18512.tsp",
   "d198.tsp",
   "d2103.tsp",
   "d493.tsp",
   "d657.tsp",
   "dantzig42.tsp",
   "dsj1000.tsp",
   "eil101.tsp",
   "eil51.tsp",
   "eil76.tsp",
   "fl417.tsp",
   "fri26.tsp",
   "gil262.tsp",
   "gr120.tsp",
   "gr137.tsp",
   "gr17.tsp",
   "gr202.tsp",
   "gr21.tsp",
   "gr229.tsp",
   "gr24.tsp",
   "gr431.tsp",
   "gr48.tsp",
   "gr666.tsp",
   "gr96.tsp",
   "hk48.tsp",
   "kroA100.tsp",
   "kroA150.tsp",
   "kroA200.tsp",
   "kroB100.tsp",
   "kroB150.tsp",
   "kroB200.tsp",
   "kroC100.tsp",
   "kroD100.tsp",
   "kroE100.tsp",
   "lin105.tsp",
   "lin318.tsp",
   "linhp318.tsp",
   "nrw1379.tsp",
   "p654.tsp",
   "pa561.tsp",
   "pcb1173.tsp",
   "pcb3038.tsp",
   "pcb442.tsp",
   #"pla33810.tsp",
   #"pla7397.tsp",
   #"pla85900.tsp",
   "pr1002.opt.tour",
   "pr1002.tsp",
   "pr107.tsp",
   "pr124.tsp",
   "pr136.tsp",
   "pr144.tsp",
   "pr152.tsp",
   "pr226.tsp",
   "pr2392.opt.tour",
   "pr2392.tsp",
   "pr264.tsp",
   "pr299.tsp",
   "pr439.tsp",
   "pr76.opt.tour",
   "pr76.tsp",
   "rat195.tsp",
   "rat575.tsp",
   "rat783.tsp",
   "rat99.tsp",
   "rat99.tsp",
   "rd100.opt.tour",
   "rd100.tsp",
   "rd400.tsp",
   #"rl11849.tsp",
   #"rl1304.tsp",
   #"rl1323.tsp",
   #"rl1889.tsp",
   #"rl5915.tsp",
   #"rl5934.tsp",
   "si1032.tsp",
   "si175.tsp",
   "si535.tsp",
   "st70.opt.tour",
   "st70.tsp",
   "swiss42.tsp",
   "ts225.tsp",
   "tsp225.opt.tour",
   "tsp225.tsp",
   "u1060.tsp",
   "u1432.tsp",
   "u159.tsp",
   "u1817.tsp",
   "u2152.tsp",
   "u2319.tsp",
   "u574.tsp",
   "u724.tsp",
   "ulysses16.opt.tour",
   "ulysses16.tsp",
   "ulysses22.opt.tour",
   "ulysses22.tsp",
   "usa13509.tsp",
   "vm1084.tsp",
   "vm1748.tsp" 
]
LIST_OF_ASYMETRIC_PROBLEM=[
   "ft53.atsp",
   "ft70.atsp",
   "ftv170.atsp",
   "ftv33.atsp",
   "ftv35.atsp",
   "ftv38.atsp",
   "ftv44.atsp",
   "ftv47.atsp",
   "ftv55.atsp",
   "ftv64.atsp",
   "ftv70.atsp",
   "kro124p.atsp",
   "p43.atsp",
   "rbg323.atsp",
   "rbg358.atsp",
   "rbg403.atsp",
   "rbg443.atsp",
   "ry48p.atsp"
]

TIME_STSP=[
     222.4540968,
    459.184829,
    40.51870322,
    469.4082878,
    23.23392987,
    42.90524936,
    104.6625633,
    56.32049179,
    128.3025324,
    14.73703098,
    97.14068747,
    115.1928775,
    1311.237344,
    148.5524726,
    2263.325935,
    382.8074281,
    573.3130093,
    30.31174111,
    1032.644655,
    81.25562549,
    49.7430439,
    65.71297789,
    369.7335258,
    37.4608376,
    218.8284681,
    89.69264269,
    109.5394042,
    18.84800053,
    159.5924096,
    27.24211025,
    185.5460348,
    34.14074159,
    536.2212975,
    68.72836661,
    1042.802424,
    68.42189336,
    40.96043158,
    78.79397202,
    114.2652745,
    155.9017153,
    84.52374125,
    118.7779369,
    161.6775532,
    90.34395075,
    94.48477149,
    97.39115572,
    102.9908712,
    281.3688676,
    282.5278668,
    1438.352993,
    596.4418008,
    463.6923509,
    1207.700351,
    3653.915233,
    398.2390203,
    1056.82181
]


if __name__ == '__main__':
    print("Start test")

    list_small_stsp=["burma14.tsp","gr17.tsp","ulysses16.tsp","gr21.tsp","ulysses22.tsp","gr24.tsp"]
    #performance for approximative algo
    path = ROOT_PATH_ATSP + LIST_OF_SYMETRIC_PROBLEM[21]
    #print(path)
    tsp_file=open(path,'r')
    parser = Parser()
    matrix = parser.parse_file(tsp_file)
    #print(matrix)
    #parser.print_nicely(matrix)
    algo_list=["Brute Force","Branch and Bound","Minimum Spanning Tree","Genetic","Add and Remove Edges","Greedy","Dynamic","Random","Ant Colony"]
    algo_approx=["Minimum Spanning Tree","Genetic","Add and Remove Edges","Greedy","Random","Ant Colony"]
    algo_opt=["Brute Force","Branch and Bound","Add and Remove Edges","Dynamic"]
    algo_list=["Dynamic"]
    root='E:\\Dev\\MLDMProoject\\Code\\'

    for i in range(40,len(TIME_STSP)):
        if '.opt.' in LIST_OF_SYMETRIC_PROBLEM[i]:
            continue
        path = ROOT_PATH_ATSP + LIST_OF_SYMETRIC_PROBLEM[i]
        print(path)
        tsp_file=open(path,'r')
        parser = Parser()
        matrix = parser.parse_file(tsp_file)

        cmatrix = copy.deepcopy(matrix)
        min_cost = math.inf
        opt_path=[]
        start_time = time.time()
        while(time.time()-start_time<TIME_STSP[i]):
            algo = GreedyTsp(cmatrix)
            upper_bound, best_path, run_time = algo.greedy_tsp()
            if upper_bound < min_cost :
                min_cost = upper_bound
                opt_path = best_path
        end_time = time.time()
        foutput = open("E:\Dev\MLDMProoject\Code\All_algo_tsp3.txt",'a')
        foutput.write(LIST_OF_SYMETRIC_PROBLEM[i] + "\t" + "Greedy" + "\t" + str(min_cost) + "\t" + str(opt_path) + "\t" + str(end_time-start_time)+"\n")
        foutput.close()

        cmatrix = copy.deepcopy(matrix)
        min_cost = math.inf
        opt_path=[]
        start_time = time.time()
        while(time.time()-start_time<TIME_STSP[i]):
            algo = TspRandom(cmatrix)
            upper_bound, best_path, run_time = algo.run()
            if upper_bound < min_cost :
                min_cost = upper_bound
                opt_path = best_path

        end_time = time.time()
        foutput = open("E:\Dev\MLDMProoject\Code\All_algo_tsp3.txt",'a')
        foutput.write(LIST_OF_SYMETRIC_PROBLEM[i] + "\t" + "Random" + "\t" + str(min_cost) + "\t" + str(opt_path) + "\t" + str(end_time-start_time)+"\n")
        foutput.close()

        cmatrix = copy.deepcopy(matrix)
        min_cost = math.inf
        opt_path=[]
        start_time = time.time()
        while(time.time()-start_time<TIME_STSP[i]):
            algo = MST(cmatrix)
            upper_bound, best_path, run_time = algo.mst()
            if upper_bound < min_cost :
                min_cost = upper_bound
                opt_path = best_path
        end_time = time.time()
        foutput = open("E:\Dev\MLDMProoject\Code\All_algo_tsp3.txt",'a')
        foutput.write(LIST_OF_SYMETRIC_PROBLEM[i] + "\t" + "Minimum Spanning Tree" + "\t" + str(min_cost) + "\t" + str(opt_path) + "\t" + str(end_time-start_time)+"\n")
        foutput.close()

    # for pb in list_small_stsp:
    #     path = ROOT_PATH_ATSP + pb
    #     print(path)
    #     tsp_file=open(path,'r')
    #     parser = Parser()
    #     matrix = parser.parse_file(tsp_file)




        # for algo_sel in algo_list:
        #     print(algo_sel)
        #     cmatrix = copy.deepcopy(matrix)
        #     if algo_sel == "Brute Force":
        #         brute = Brute(cmatrix)
        #         upper_bound, best_path, run_time = brute.algo()
        #
        #     if algo_sel == "Branch and Bound":
        #         algo = BranchAndBound()
        #         upper_bound, best_path, run_time = algo.run_branch_and_bound(cmatrix)
        #
        #     elif algo_sel == "Minimum Spanning Tree":
        #         algo = MST(cmatrix)
        #         upper_bound, best_path, run_time = algo.mst()
        #
        #     elif algo_sel == "Genetic":
        #         algo = Genetic(cmatrix,50,100)
        #         upper_bound, best_path, run_time = algo.main()
        #
        #     elif algo_sel == "Add and Remove Edges":
        #         algo = AddRemoveEdges(cmatrix)
        #         upper_bound, best_path, run_time = algo.main()
        #
        #     elif algo_sel == "Greedy":
        #         algo = GreedyTsp(cmatrix)
        #         upper_bound, best_path, run_time = algo.greedy_tsp()
        #
        #     elif algo_sel == "Dynamic":
        #         algo = TspDp(cmatrix)
        #         upper_bound, best_path, run_time = algo.run()
        #
        #     elif algo_sel == "Random":
        #         algo = TspRandom(cmatrix)
        #         upper_bound, best_path, run_time = algo.run()
        #
        #     elif algo_sel == "Ant Colony":
        #         algo = AntApproach(cmatrix,iteration=500)
        #         upper_bound, best_path, run_time = algo.algo()
        #
        #     print(algo_sel,upper_bound, best_path, run_time )
        #     foutput = open("E:\Dev\MLDMProoject\Code\All_algo_tsp2.txt",'a')
        #     foutput.write(pb + "\t" + algo_sel + "\t" + str(upper_bound) + "\t" + str(best_path) + "\t" + str(run_time)+"\n")
        #     foutput.close()
