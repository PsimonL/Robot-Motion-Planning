import numpy as np

from Graph_Algorithms.ConstVars import NUM_ROWS, NUM_COLS
from Nodes import Nodes
from Graph_Algorithms.GeometryUtils import is_node_inside_obstacle, is_node_inside_room


def create_grid(obstacles_coords, room_coords) -> list:
    grid = []
    nodes_id = 1
    nodes_outside_room = 1

    obstacles_coords_np = np.array(obstacles_coords)  # Konwersja na tablicę Numpy

    for row in range(1, NUM_ROWS - 1):
        for col in range(1, NUM_COLS - 1):
            x = col * 5
            y = row * 5
            if is_node_inside_room((x, y), room_coords):
                node = Nodes(x, y, row, col, nodes_id)
                nodes_id += 1
                grid.append(node)
                # print(f"APPENDED Node {node.node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")
            else:
                node = Nodes(-1, -1, -1, -1, nodes_id)
                nodes_id += 1
                nodes_outside_room += 1
                grid.append(node)
                # print(f"DELETED Node {node.node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")

    set_neighbours(grid, obstacles_coords_np)  # Przekazanie przekształconej tablicy Numpy

    print(f"Grid set. {nodes_id - nodes_outside_room} nodes.")
    return grid


def set_neighbours(grid, obstacles_coords):
    counter = 1
    for node in grid:
        row, col = node.row, node.col
        x, y = node.x, node.y
        if row == col == x == y == -1:
            # print("PASS OVER NODE")
            continue

        neighbors = []

        # print( f"========== NODE {counter} - {node.node_id} (r, c) = ({row}, {col}) ; (x, y) = ({node.x},
        # {node.y}) ==========")

        # Directions: [D, U, R, L, DR, UL, UR, DL]
        neighbor_direction = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in neighbor_direction:
            # print(f"dr, dc = {dr}, {dc}")
            if row != -1 and col != -1:
                r, c = row + dr, col + dc
                if 1 <= r < NUM_ROWS - 1 and 1 <= c < NUM_COLS - 1:
                    neighbor_node = grid[((r - 1) * (NUM_COLS - 2) + c) - 1]
                    # print(f"(({r} - 1) * ({NUM_COLS} - 2) + {c}) - 1 = {((r - 1) * (NUM_COLS - 2) + c) - 1}")
                    if not is_node_inside_obstacle(neighbor_node, obstacles_coords):
                        neighbors.append(neighbor_node)
        node.neighbours_lst = neighbors
        counter += 1


def find_nodes_by_coordinates(grid, x, y):
    for node in grid:
        if node.x == x and node.y == y:
            return node
    return None
