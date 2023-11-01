import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from numba import jit
import time
import multiprocessing

size = 650
inner_size = 600
WIDTH, HEIGHT = size, size
INNER_WIDTH, INNER_HEIGHT = inner_size, inner_size
ADJUST_VECTOR = (size - inner_size) // 2

NODE_SIZE = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

NUM_ROWS = ((INNER_WIDTH) // 5) + 1
NUM_COLS = ((INNER_HEIGHT) // 5) + 1
# NUM_ROWS = INNER_WIDTH
# NUM_COLS = INNER_HEIGHT

THRASH_NODES = set()


# class Environment:
#     def __init__(self):


class Nodes:
    def __init__(self, x, y, row, col):
        self.x, self.y = x, y  # row, col
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        self.G, self.H = 0, 0  # G - distance from current node to start node , H - heuristic distance from current node to end node
        self.F = self.G + self.H  # F (node in nodes) = G (node in nodes) + H (node in nodes)
        self.parent_ptr = 0
        self.neighbours_lst = []

    def __str__(self):
        return f"Node at ({self.x}, {self.y}) - Row: {self.row}, Col: {self.col}"


def ret_distance(p1: tuple, p2: tuple) -> int:  # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    dx, dy = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    D, D2 = 5, 7  # cost 5 for horizontal and vertical, cost 7 for diagonal
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)  # Diagonal Distance


def get_obstacles(obstacles):
    obstacle_rects = []
    for obstacle in obstacles:
        if isinstance(obstacle[0], list):
            for sub_obstacle in obstacle:
                obstacle_rects.append(pygame.Rect(sub_obstacle[0], sub_obstacle[1], sub_obstacle[2], sub_obstacle[3]))
        else:
            obstacle_rects.append(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
    return obstacle_rects

def is_inside_room(point, room_coords):
    polygon = Polygon(room_coords)
    point = Point(point[0], point[1])
    return polygon.contains(point)

def check_obstacles(node, obstacles_coords):
    node_x, node_y = node.x, node.y
    for obstacles_coord in obstacles_coords:
        obstacle_x, obstacle_y, width, height = obstacles_coord
        if obstacle_x <= node_x < obstacle_x + width and obstacle_y <= node_y < obstacle_y + height:
            THRASH_NODES.add(node)
            return True
    return False


def create_grid(obstacles_coords) -> list:
    grid = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            x = col * 5
            y = row * 5
            node = Nodes(x, y, row, col)
            grid.append(node)

    print("Grid set.")

    set_neighbours(grid, obstacles_coords)
    print("Neighbours set.")

    return grid


def set_neighbours(grid, obstacles_coords):
    for node in grid:
        row, col = node.row, node.col
        neighbors = []

        # Directions: [D, U, R, L, DR, UL, UR, DL]
        neighbor_direction = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

        for dr, dc in neighbor_direction:
            r, c = row + dr, col + dc
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS:
                neighbor_node = grid[r * NUM_COLS + c]
                if not check_obstacles(neighbor_node, obstacles_coords):
                    neighbors.append(neighbor_node)

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
    while len(open_set) > 0:
        current_node = open_set[0]
        for node in open_set:
            if node.F < current_node.F or node.F == current_node.F and node.H < current_node.H:
                current_node = node

        if current_node == goal:
            path = []
            while current_node is not None:
                if isinstance(current_node, int):
                    break
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
    return None


def ui_runner(start_pt, goal_pt, grid, obstacles, path):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for node in grid:
            pygame.draw.circle(screen, WHITE, (node.x + ADJUST_VECTOR, node.y + ADJUST_VECTOR), NODE_SIZE)

        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE,
                             (obstacle[0] + ADJUST_VECTOR, obstacle[1] + ADJUST_VECTOR, obstacle[2], obstacle[3]))

        pygame.draw.circle(screen, YELLOW, (start_pt[0] + ADJUST_VECTOR, start_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)
        pygame.draw.circle(screen, GREEN, (goal_pt[0] + ADJUST_VECTOR, goal_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)

        pygame.draw.circle(screen, RED, (INNER_WIDTH + ADJUST_VECTOR, INNER_HEIGHT + ADJUST_VECTOR), NODE_SIZE * 10)

        if path:
            adjusted_path = [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in path]
            for i in range(1, len(adjusted_path)):
                pygame.draw.line(screen, RED, adjusted_path[i - 1], adjusted_path[i], NODE_SIZE * 4)

        if len(room_coords) > 1:
            pygame.draw.lines(screen, ORANGE, True,
                              [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in room_coords], NODE_SIZE * 4)

        pygame.display.update()

    pygame.quit()


# def create_grid_helper(args):
#     obstacles_coords, start, end, NUM_COLS = args
#     grid = []
#     for row in range(start, end):
#         for col in range(NUM_COLS):
#             if row * NUM_COLS + col < len(grid):
#                 # x = MARGIN_X + col * 5
#                 # y = MARGIN_Y + row * 5
#                 # node = Nodes(x, y, row, col)
#                 # grid.append(node)
#                 node = Nodes(0, 0, row, col)
#                 grid.append(node)
#
#     set_neighbours(grid, obstacles_coords)
#
#     return grid
#
# def create_grid_parallel(obstacles_coords) -> list:
#     grid = []
#
#     processes = 2  # Dwa procesy
#     pool = multiprocessing.Pool(processes)
#
#     split = NUM_ROWS // processes
#     starts = [i * split for i in range(processes)]
#     ends = [(i + 1) * split if i < processes - 1 else NUM_ROWS for i in range(processes)]
#
#     args = [(obstacles_coords, starts[i], ends[i], NUM_COLS) for i in range(processes)]
#     results = pool.map(create_grid_helper, args)
#
#     for result in results:
#         grid.extend(result)
#
#     pool.close()
#     pool.join()
#
#     return grid



if __name__ == "__main__":
    start_point = (200, 200)
    goal_point = (400, 400)

    room_coords = [(0, 0), (300, 0), (300, 50), (600, 50), (600, 600), (0, 600)]

    # obstacles_coords = [[0, 100, 400, 50], [0, 400, 200, 100], [50, 220, 600, 50]]
    obstacles_coords = []
    obstacles = get_obstacles(obstacles_coords)

    # start_time = time.time()
    grid = create_grid(obstacles_coords)

    node_id = 0
    for node in grid:
        print(f"Node {node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")
        node_id += 1

    # end_time = time.time()
    # print("Single process ", end_time - start_time)
    # start_time_m = time.time()
    # grid_m = create_grid_parallel(obstacles_coords)
    # end_time_m = time.time()
    # print("Double processes ", end_time_m - start_time_m)

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])

    sorted_thrash_set = sorted(THRASH_NODES, key=lambda node: (node.x, node.y))
    for item in sorted_thrash_set:
        print("Thrash node: {}".format(item))

    if start_node and goal_node:
        print("Starting A*")
        ret_path = a_star(start_node, goal_node)
    else:
        raise Exception("Nodes don't found!")

    if ret_path:
        print("Path found.")
        print(ret_path)
    else:
        print("Path not found!")
        print(ret_path)

    ui_runner(start_point, goal_point, grid, obstacles, ret_path)
