class TreeNode:
    def __init__(self, id, vertex_id, reduced_matrix, cost, matrix_index, path_so_far, parent_node_id, no_of_children):
        self.node_id = id
        self.vertex_id = vertex_id
        self.parent_node_id = parent_node_id
        self.reduced_matrix = reduced_matrix
        self.cost = cost
        self.index_in_matrix = matrix_index
        self.path_so_far = path_so_far
        self.number_of_children = no_of_children
        self.status = "unsearched"


