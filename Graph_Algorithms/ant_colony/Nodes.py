class Nodes:
    def __init__(self, x, y, row, col, node_id):
        self.x, self.y = x, y  # row, col
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        self.parent_ptr = 0
        self.node_id = node_id
        self.neighbours_lst = []

    def __str__(self):
        return f"Node at ({self.x}, {self.y}) - Row: {self.row}, Col: {self.col}"
