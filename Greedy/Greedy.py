import math
import time


class GreedyTsp( object ):
    def __init__(self, matrix):
        self.matrix = matrix

    def greedy_tsp(self):
        start_time = time.time()
        tour = [0]
        total_cost = 0

        visited_nodes = [(0, 0)]
        row = self.matrix[0]

        while len(visited_nodes) < len(self.matrix):

            for node in visited_nodes:
                row[node[0]] = math.inf


            min_weight = min([x for x in row if x > 0])

            visit = row.index(min_weight), min_weight
            visited_nodes.append(visit)

            tour.append(visit[0])
            total_cost += visit[1]

            row = self.matrix[visit[0]]

        total_cost += self.matrix[tour[-1]][0] if self.matrix[tour[-1]][0] < math.inf else 0
        tour.append(0)
        end_time = time.time()
        tour = [node + 1 for node in tour]
        return total_cost, tour, (end_time-start_time)


    def run_time_limit_iteration(self, time_limit, start_node):
        elapse_time = 0
        start_time=time.time()
        min_cost = float("inf")
        opt_path=[]
        while (time.time()-start_time)<time_limit:
            cost, path, time_elapse = self.greedy_tsp()
            if cost<min_cost:
                min_cost = cost
                opt_path = path

        end_time = time.time()
        return min_cost, opt_path, (end_time-start_time)


if __name__ == '__main__':
    # Run Example
    import csv
    import Parser
    from os import listdir
    from os.path import isfile, join

    parser = Parser.Parser()
    with open('greedy_results_symmetric.csv', mode='w') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(['Problem Name', ' Dimensions', ' Solution Cost', ' Run Time (Milliseconds)'])
        directory = 'tsp_symmetric'

        tsp_files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in tsp_files:
            f = open(directory + '/' + file, 'r')

            print(file)
            try:
                matrix = parser.parse_file(f)

                g = GreedyTsp(matrix)
                start_time = time.time()
                cost, tour, runtime = g.greedy_tsp()
                runtime = runtime * 1000
                results_writer.writerow([file, ' ' + str(len(matrix)), ' ' + str(cost), ' ' + str(runtime)])
            except:
                results_writer.writerow([file, ' ' + 'Error Parsing'])
