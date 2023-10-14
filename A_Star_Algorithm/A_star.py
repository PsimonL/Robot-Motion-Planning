import pygame
import math

WIDTH = 600
HEIGHT = 600

NODE_SIZE = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Node 0 at (10, 10) - Row: 0, Col: 0
# Node 3570 at (610, 610) - Row: 30, Col: 30
# MARGIN_X = 10
# MARGIN_Y = 10
MARGIN_X = 0
MARGIN_Y = 0
NUM_ROWS = (WIDTH - MARGIN_X) // 5
NUM_COLS = (HEIGHT - MARGIN_Y) // 5


class Nodes:
    def __init__(self, x, y, row, col):
        self.x, self.y = x, y
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        self.G, self.H = 0, 0  # G - distance from current node to start node , H - heuristic distance from current node to end node
        self.F = self.G + self.H  # F (node in nodes) = G (node in nodes) + H (node in nodes)
        self.parent_ptr = 0
        self.neighbours_lst = []

    # def __str__(self):
    #     return f"Node at ({self.x}, {self.y}) - Row: {self.row}, Col: {self.col}"


def ret_distance(p1: tuple, p2: tuple) -> int:  # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    dx, dy = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    D, D2 = 5, 7  # cost 5 for horizontal and vertical, cost 7 for diagonal
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)  # Diagonal Distance


def create_grid() -> list:
    grid = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = MARGIN_X + col * 20
            y = MARGIN_Y + row * 20
            node = Nodes(x, y, row, col)
            grid.append(node)

    print("Grid set.")

    set_neighbours(grid)
    print("Neighbours set.")
    # node_id = 0
    # for node in grid:
    #    print(f"Node {node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")
    #    node_id += 1

    return grid


def set_neighbours(grid):
    for node in grid:
        row, col = node.row, node.col
        neighbors = []

        # Directions: [D, U, R, L, DR, UL, UR, DL]
        neighbor_direction = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in neighbor_direction:
            r, c = row + dr, col + dc
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
                neighbors.append(grid[r * NUM_COLS + c])

        node.neighbours_lst = neighbors


def find_nodes_by_coordinates(grid, x, y):
    for node in grid:
        if node.x == x and node.y == y:
            return node
    return None


def a_star(start, goal):  # https://en.wikipedia.org/wiki/A*_search_algorithm
    open_set = []
    close_set = []

    open_set.append(start)
    # print(f"1st append : {[node.__str__() for node in open_set]}")
    counter = 0
    while len(open_set) > 0:
        current_node = open_set[0]
        for node in open_set:
            if node.F < current_node.F or node.F == current_node.F and node.H < current_node.H:
                current_node = node

        if current_node == goal:
            print("if current_node == goal:")
            path = []
            while current_node is not None:
                print("while current_node is not None:")
                if isinstance(current_node, int):
                    print("int")
                    break
                print(type(current_node))
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent_ptr
            return path[::-1]

        close_set.append(current_node)
        open_set.remove(current_node)

        for neighbor in current_node.neighbours_lst:
            if neighbor in close_set:
                continue

            tentative_g_score = current_node.G + ret_distance((current_node.x, current_node.y),
                                                              (neighbor.x, neighbor.y))
            neighbor.parent_ptr = current_node
            neighbor.G = tentative_g_score
            neighbor.H = ret_distance((neighbor.x, neighbor.y), (goal.x, goal.y))
            neighbor.F = neighbor.G + neighbor.H

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= neighbor.G:
                continue
        # print(counter)
        counter += 1

    return None


def ui_runner(start_pt, goal_pt, grid, path):

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for node in grid:
            pygame.draw.circle(screen, WHITE, (node.x, node.y), NODE_SIZE)

        pygame.draw.circle(screen, YELLOW, (start_pt[0], start_pt[1]), NODE_SIZE * 8)
        pygame.draw.circle(screen, GREEN, (goal_pt[0], goal_pt[1]), NODE_SIZE * 8)

        if path:
            for i in range(1, len(path)):
                pygame.draw.line(screen, RED, path[i - 1], path[i], NODE_SIZE * 4)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    start_point = (100, 100)
    goal_point = (300, 100)

    grid = create_grid()

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])
    print(start_node)
    # print(start_node.x)
    # print(start_node.y)
    # print(start_node.row)
    # print(start_node.col)
    # print(start_node.F)
    # print(start_node.G)
    # print(start_node.H)
    # print(start_node.parent_ptr)
    # print(start_node.neighbours_lst)

    print("Starting A*")
    ret_path = a_star(start_node, goal_node)

    if ret_path:
        print("Path found.")
        print(ret_path)
    else:
        print("Path not found!")
        print(ret_path)

    ui_runner(start_point, goal_point, grid, ret_path)
