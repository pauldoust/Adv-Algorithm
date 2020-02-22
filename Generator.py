import math
import pickle
import random


class Generator:
    # Generate a TSP problem represented in an NxN matrix, given:
    # nodes: the number of cities (dimensions of the matrix "N"). [int]
    # connectivity: specifies the level of sparsity in the problem. bounds: (2 < connectivity < nodes). [int]
    # min_weight/max_weight: bounds of the randomly generated weights (values of matrix entries). [int], [int]
    # symmetric: defines whether the problem is symmetric or not. [bool].
    def generate(self, nodes, connectivity, min_weight, max_weight, symmetric):
        k = 0
        matrix = []
        for j in range(nodes):
            matrix.append([-1 if i != k else math.inf for i in range(nodes)])
            k += 1

        for i in range(len(matrix)):
            indexes = []
            for index, element in enumerate(matrix[i]):
                if element == -1:
                    indexes.append(index)


            if connectivity - 1 < len(indexes):
                rand_nodes = random.sample(indexes[1:], connectivity - 1)
                rand_nodes.insert(0, i+1 if i+1 < len(matrix) else 0)
            else:
                rand_nodes = indexes

            for cell in rand_nodes:
                weight = random.randint(min_weight, max_weight)
                matrix[i][cell] = weight
                if symmetric:
                    matrix[cell][i] = weight

        return matrix


    # Save the matrix to local file, given the matrix and and file directory/name.
    def save_to_file(self, matrix, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(matrix, f)


    # Read a matrix from a local file saved by the previous method, given the file directory/name.
    def read_from_file(self, file_name):
        with open(file_name, 'rb') as f:
            matrix = pickle.load(f)

        return matrix

    # Print the matrix in an easy to read format
    def print_nicely(self, matrix):
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))


# RUN EXAMPLE:

# Create a new generator.
#generator = Generator()

# Generate a new matrix with given parameters.
#matrix = generator.generate(8, 2, 2, 9999, True)

# Save the matrix locally.
#generator.save_to_file(matrix, 'test_files/test_matrix')

# Read and print the matrix
#matrix = generator.read_from_file('test_files/test_matrix')

#generator.print_nicely(matrix)
