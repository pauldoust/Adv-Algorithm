import math


class Parser:

    # Read specification part of the problem file
    def parse_file(self, file):
        problem_name = ''
        nodes_no = 0
        edges_type = ''
        for line in file:
            if line.startswith('NAME'):
                problem_name = line[line.index(':')+2:]

            if line.startswith('DIMENSION'):
                nodes_no = int(line[line.index(':')+2:])

            if line.startswith('EDGE_WEIGHT_TYPE'):
                edges_type = (line[line.index(':')+2:]).rstrip()

            if line.startswith('EDGE_WEIGHT_FORMAT'):
                matrix_type = line[line.index(':')+2:]
                edges_type = edges_type.rstrip() + ' - ' + matrix_type.rstrip()

            if line.startswith('NODE_COORD_SECTION') or line.startswith('EDGE_WEIGHT_SECTION'):
                break

        return self.gen_matrix(file, edges_type, nodes_no)


    # Read COORD part of the problem file and generate the weights matrix
    def gen_matrix(self, file, type, dimensions):

        if type.startswith('EUC_2D'):
            return self.euc_2d_matrix(file)
        if type.startswith('CEIL_2D'):
            return self.ceil_2d_matrix(file)
        if type.startswith('GEO'):
            return self.geographical_matrix(file)
        if type.startswith('ATT'):
            return self.pseudo_euc_matrix(file)
        if type.startswith('EXPLICIT'):
            if type.endswith('UPPER_ROW'):
                return self.matrix_upper_row(file, dimensions)
            if type.endswith('LOWER_ROW'):
                return self.matrix_lower_row(file, dimensions)
            if type.endswith('UPPER_DIAG_ROW'):
                return self.matrix_upper_diag_row(file, dimensions)
            if type.endswith('LOWER_DIAG_ROW'):
                return self.matrix_lower_diag_row(file, dimensions)
            if type.endswith('FULL_MATRIX'):
                return self.matrix_full(file, dimensions)



    def euc_2d_matrix(self, file):
        matrix = []
        coord_data = []

        for line in file:
            if 'DISPLAY_DATA_SECTION' in line or 'EOF' in line:
                break
            values = list(filter(None, line.split(' ')))
            values[0] = int(values[0])
            values[1] = int(float(values[1]))
            values[2] = int(float(values[2]))
            coord_data.append(values)

        for node in coord_data:
            row_index = node[0]
            row_x = node[1]
            row_y = node[2]
            matrix_row = []

            for cell in coord_data:
                cell_index = cell[0]
                cell_x = cell[1]
                cell_y = cell[2]

                if cell_index == row_index:
                    matrix_row.append(math.inf)
                    continue
                xd = row_x - cell_x
                yd = row_y - cell_y
                sqr = math.sqrt(xd*xd + yd*yd)
                matrix_row.append(int(sqr))

            matrix.append(matrix_row)

        return matrix


    def ceil_2d_matrix(self, file):
        matrix = []
        coord_data = []

        for line in file:
            if 'DISPLAY_DATA_SECTION' in line or 'EOF' in line:
                break
            values = list(filter(None, line.split(' ')))
            values[0] = int(values[0])
            values[1] = int(float(values[1]))
            values[2] = int(float(values[2]))
            coord_data.append(values)

        for node in coord_data:
            row_index = node[0]
            row_x = node[1]
            row_y = node[2]
            matrix_row = []

            for cell in coord_data:
                cell_index = cell[0]
                cell_x = cell[1]
                cell_y = cell[2]

                if cell_index == row_index:
                    matrix_row.append(math.inf)
                    continue
                xd = row_x - cell_x
                yd = row_y - cell_y
                sqr = math.sqrt(xd*xd + yd*yd)
                matrix_row.append(math.ceil(sqr))

            matrix.append(matrix_row)

        return matrix


    def geographical_matrix(self, file):
        PI = 3.141592
        RRR = 6378.388

        coord_data = []

        for line in file:
            if 'DISPLAY_DATA_SECTION' in line or 'EOF' in line:
                break

            # Calculate and store Longitude and Latitude

            # Index
            values = list(filter(None, line.split(' ')))
            values[0] = int(values[0])

            # Latitude
            values[1] = float(values[1])
            deg = int(values[1])
            min = values[1] - deg
            values[1] = PI * (deg + 5.0 * min / 3.0) / 180.0

            # Longitude
            values[2] = float(values[2])
            deg = int(values[2])
            min = values[2] - deg
            values[2] = PI * (deg + 5.0 * min / 3.0) / 180.0

            coord_data.append(values)

        matrix = []
        for node in coord_data:
            row_index = node[0]
            row_latitude = node[1]
            row_longitude = node[2]

            matrix_row = []
            for cell in coord_data:
                cell_index = cell[0]
                cell_latitude = cell[1]
                cell_longitude = cell[2]

                if cell_index == row_index:
                    matrix_row.append(math.inf)
                    continue

                q1 = math.cos(row_longitude - cell_longitude)
                q2 = math.cos(row_latitude - cell_latitude)
                q3 = math.cos(row_latitude + cell_latitude)
                distance = RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0

                matrix_row.append(int(distance))

            matrix.append(matrix_row)

        return matrix


    def pseudo_euc_matrix(self, file):
        matrix = []
        coord_data = []

        for line in file:
            if 'DISPLAY_DATA_SECTION' in line or 'EOF' in line:
                break
            values = list(filter(None, line.split(' ')))
            values[0] = int(values[0])
            values[1] = int(float(values[1]))
            values[2] = int(float(values[2]))
            coord_data.append(values)

        for node in coord_data:
            row_index = node[0]
            row_x = node[1]
            row_y = node[2]
            matrix_row = []

            for cell in coord_data:
                cell_index = cell[0]
                cell_x = cell[1]
                cell_y = cell[2]

                if cell_index == row_index:
                    matrix_row.append(math.inf)
                    continue
                xd = row_x - cell_x
                yd = row_y - cell_y
                rij = math.sqrt((xd*xd + yd*yd) / 10.0)
                tij = int(rij)
                if tij < rij:
                    matrix_row.append((tij + 1))
                else:
                    matrix_row.append(tij)

            matrix.append(matrix_row)


        return matrix


    def matrix_upper_row(self, file, dimensions):
        separated_str_values = file.read().replace('\n', '').replace('\r', '').replace('EOF', '').split(' ')
        values = [int(x) for x in list(filter(None, separated_str_values))]

        matrix = []
        k = 0
        for j in range(dimensions):
            matrix.append([-1 if i != k else math.inf for i in range(dimensions)])
            k += 1

        i = 0
        j = 1
        for index, value in enumerate(values):
            if value == 0:
                if i == j:
                    value = math.inf
                else:
                    value = -1

            matrix[i][j] = value
            matrix[j][i] = value

            if j == dimensions - 1:
                i += 1
                j = i + 1
            else:
                j += 1

        return matrix


    def matrix_lower_row(self, file, dimensions):
        separated_str_values = file.read().replace('\n', '').replace('\r', '').replace('EOF', '').split(' ')
        values = [int(x) for x in list(filter(None, separated_str_values))]

        matrix = []
        k = 0
        for j in range(dimensions):
            matrix.append([-1 if i != k else math.inf for i in range(dimensions)])
            k += 1

        i = 1
        j = 0
        for index, value in enumerate(values):
            if value == 0:
                if i == j:
                    value = math.inf
                else:
                    value = -1

            matrix[i][j] = value
            matrix[j][i] = value

            if j == i - 1:
                i += 1
                j = 0
            else:
                j += 1

        return matrix


    def matrix_upper_diag_row(self, file, dimensions):
        separated_str_values = file.read().replace('\n', '').replace('\r', '').replace('EOF', '').split(' ')
        values = [int(x) for x in list(filter(None, separated_str_values))]

        matrix = [[-1 for i in range(dimensions)] for j in range(dimensions)]

        i = 0
        j = 0
        for index, value in enumerate(values):
            if value == 0:
                if i == j:
                    value = math.inf
                else:
                    value = -1

            matrix[i][j] = value
            matrix[j][i] = value

            if j == dimensions - 1:
                i += 1
                j = i
            else:
                j += 1

        return matrix


    def matrix_lower_diag_row(self, file, dimensions):
        separated_str_values = file.read().replace('\n', '').replace('\r', '').replace('EOF', '').split(' ')
        values = [int(x) for x in list(filter(None, separated_str_values))]

        matrix = [[-1 for i in range(dimensions)] for j in range(dimensions)]

        i = 0
        j = 0
        for index, value in enumerate(values):
            if value == 0:
                if i == j:
                    value = math.inf
                else:
                    value = -1

            matrix[i][j] = value
            matrix[j][i] = value

            if j == i:
                i += 1
                j = 0
            else:
                j += 1

        return matrix


    def matrix_full(self, file, dimensions):
        separated_str_values = file.read().replace('\n', '').replace('\r', '').replace('EOF', '').split(' ')
        values = [int(x) for x in list(filter(None, separated_str_values))]

        matrix = [[-1 for i in range(dimensions)] for j in range(dimensions)]

        i = 0
        j = 0
        for index, value in enumerate(values):
            if value == 0:
                if i == j:
                    value = math.inf
                else:
                    value = -1

            matrix[i][j] = value

            if j == dimensions - 1:
                i += 1
                j = 0
            else:
                j += 1

        return matrix


    def print_nicely(self, matrix):
        s = [[str(e) for e in row] for row in matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))



# RUN EXAMPLE:

# # Open the problem file (Either .tsp or .atsp)
# file = open('C:/data/ulysses16.tsp', 'r')
#
# # Create a new generator.
# parser = Parser()
#
# # Parse the file into a weights matrix.
# matrix = parser.parse_file(file)
#
# # Print the matrix in an easy to read format.
# parser.print_nicely(matrix)
