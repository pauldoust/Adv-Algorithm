import math
import time

class Node:

    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.children = []


    def add_child(self, node):
        self.children.append(node)


    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children


    def __str__(self, level=0):
        ret = "\t" * level + 'Value: ' + repr(self.value) + ', Index: ' + repr(self.index) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'



class MST:

    def __init__(self, matrix):
        self.matrix = matrix
        self.dimension = len(matrix)


    def print_mst(self, parent):
        print("Edge \tWeight")
        for i in range(1, self.dimension):
            print(parent[i], "-", i, "\t", self.matrix[parent[i]][i])


    def construct_tree(self, parents):
        root = Node(0, 0)

        for i, node in enumerate(parents):
            if root.index == node:
                child = Node(i, self.matrix[parents[i]][i])
                child = self.construct_children(child, parents)
                root.add_child(child)
        return root


    def construct_children(self, node, parents):
        for i, value in enumerate(parents):
            if node.index == value:
                child = Node(i, self.matrix[parents[i]][i])
                child = self.construct_children(child, parents)
                node.add_child(child)
        return node


    def dfs(self, tree):
        tour = [tree.index]
        if tree.children:
            for child in tree.children:
                tour.extend(self.dfs(child))

        return tour


    def tour_cost(self, tour):
        cost = 0
        # print('tour len: ', len(tour))
        for i in range(1, len(tour)):
            # print(self.matrix[tour[i-1]][tour[i]])
            cost += self.matrix[tour[i-1]][tour[i]]

        return cost


    def get_min_key_index(self, key_values, mst_set):
        minimum_node = None
        minimum = math.inf

        for node in range(self.dimension):
            if key_values[node] < minimum and not mst_set[node]:
                minimum = key_values[node]
                minimum_node = node

        return minimum_node


    def mst(self):
        start_time = time.time()
        key_values = [math.inf for i in range(self.dimension)]
        mst_set = [False for i in range(self.dimension)]
        parents = [-1 for i in range(self.dimension)]

        key_values[0] = 0

        while mst_set.count(False) > 0:
            min_key_index = self.get_min_key_index(key_values, mst_set)
            mst_set[min_key_index] = True

            cur_row = self.matrix[min_key_index]

            for node in range(self.dimension):
                if cur_row[node] > 0 and cur_row[node] != math.inf \
                        and not mst_set[node] and key_values[node] > cur_row[node]:
                    key_values[node] = cur_row[node]
                    parents[node] = min_key_index

        # self.print_mst(parents)

        tree = self.construct_tree(parents)
        tour = self.dfs(tree)
        tour.append(0)
        cost = self.tour_cost(tour)
        end_time = time.time()
        tour = [node + 1 for node in tour]
        return cost, tour, (end_time-start_time)

    def run_time_limit_iteration(self, time_limit, start_node=0):
        start_time = time.time()
        min_cost = float("inf")
        opt_path=[]
        while (time.time()-start_time)<time_limit:
            cost, opt_path, run_time = self.mst()
            if cost<min_cost:
                min_cost = cost
                opt_path = opt_path

        end_time = time.time()
        return min_cost, opt_path, (end_time-start_time)


# Run Example
if __name__ == '__main__':
    # Run Example
    import csv
    import Parser
    from os import listdir
    from os.path import isfile, join

    parser = Parser.Parser()
    with open('mst_results_symmetric.csv', mode='w') as results_file:
        results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(['Problem Name', ' Dimensions', ' Solution Cost', ' Run Time (Milliseconds)'])
        directory = 'tsp_symmetric'

        tsp_files = [f for f in listdir(directory) if isfile(join(directory, f))]

        for file in tsp_files:
            f = open(directory + '/' + file, 'r')

            print(file)
            try:
                matrix = parser.parse_file(f)

                mst = MST(matrix)
                start_time = time.time()
                cost, tour, runtime = mst.mst()
                runtime = runtime * 1000
                results_writer.writerow([file, ' ' + str(len(matrix)), ' ' + str(cost), ' ' + str(runtime)])
            except:
                results_writer.writerow([file, ' ' + 'Error Parsing'])

