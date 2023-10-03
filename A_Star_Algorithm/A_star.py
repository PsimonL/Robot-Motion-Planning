import pygame
import math

WIDTH = 600
HEIGHT = 600

NODE_SIZE = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Nodes:
    def __init__(self, x, y, row, col):
        self.x, self.y = x, y
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        # G - distance from current node to start node , H - heuristic distance from current node to end node
        self.G, self.H = 0, 0
        self.F = self.G + self.H  # F (node in nodes) = G (node in nodes) + H (node in nodes)
        self.parent_ptr = 0
        self.neighbours = []

    def __str__(self):
        return f"Node at ({self.x}, {self.y}) - Row: {self.row}, Col: {self.col}"

def get_neighbours(node):
    return []


def set_G():
    pass


def set_H():
    pass


def ret_distance(p1: tuple, p2: tuple) -> int:  # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    dx, dy = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    D, D2 = 5, 7  # cost 5 for horizontal and vertical, cost 7 for diagonal
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)  # Diagonal Distance


def a_star(start, goal):  # https://en.wikipedia.org/wiki/A*_search_algorithm
    open_set = []
    close_set = []

    start_node = start
    goal_node = goal

    open_set.append(start_node)

    # while len(open_set) > 0:
    while any(open_set):
        current_node = open_set[0]
        for node in open_set:
            if node.F < current_node.F or node.F == current_node.F and node.H < current_node.H:
                current_node = node

        if current_node == goal:
            path = []
            current = current_node
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent_ptr
            return path[::-1]

        close_set.append(current_node)
        open_set.remove(current_node)

        for neighbor in current_node.neighbours:
            if neighbor in close_set:
                continue

            tentative_g_score = current_node.G + ret_distance((current_node.x, current_node.y),
                                                              (neighbor.x, neighbor.y))
            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= neighbor.G:
                continue

            neighbor.parent_ptr = current_node
            neighbor.G = tentative_g_score
            neighbor.H = ret_distance((neighbor.x, neighbor.y), (goal_node.x, goal_node.y))
            neighbor.F = neighbor.G + neighbor.H

    return None


def create_grid() -> list:
    # Node 0 at (10, 10) - Row: 0, Col: 0
    # Node 3570 at (610, 610) - Row: 30, Col: 30
    # margin_x = 10
    # margin_y = 10
    margin_x = 0
    margin_y = 0
    num_rows = (WIDTH - margin_x) // 5
    num_cols = (HEIGHT - margin_y) // 5

    # print(f"num_rows = {num_rows}")
    # print(f"num_cols = {num_cols}")

    grid = []
    for row in range(num_rows):
        for col in range(num_cols):
            x = margin_x + col * 20
            y = margin_y + row * 20
            node = Nodes(x, y, row, col)
            grid.append(node)

    node_id = 0
    for node in grid:
        # print(f"Node {node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")
        node_id += 1

    return grid


def ui_runner():
    grid = create_grid()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for node in grid:
            pygame.draw.circle(screen, WHITE, (node.x, node.y), NODE_SIZE)

        pygame.display.update()

    pygame.quit()


def find_nodes_by_coordinates(grid, x, y):
    for node in grid:
        if node.x == x and node.y == y:
            return node
    return None


if __name__ == "__main__":
    ui_runner()
    # print(ret_distance((100, 100), (105, 105)))

    start_point = find_nodes_by_coordinates(grid=create_grid(), x=100, y=100)
    goal_point = find_nodes_by_coordinates(grid=create_grid(), x=300, y=300)

    path = a_star(start_point, goal_point)

    if path:
        print("Path found.")
        print(path)
    else:
        print("Path not found!")
        print(path)
