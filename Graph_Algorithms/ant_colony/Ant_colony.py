# TODO: change list for numpy arrays
# TODO: reafctor code for CUDA GPU

import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from numba import cuda, jit
import numpy as np
import time
import random
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

# NUM_ROWS = ((INNER_WIDTH) // 100) + 1
# NUM_COLS = ((INNER_HEIGHT) // 100) + 1
NUM_ROWS = ((INNER_WIDTH) // 5) + 1
NUM_COLS = ((INNER_HEIGHT) // 5) + 1
# NUM_ROWS = INNER_WIDTH
# NUM_COLS = INNER_HEIGHT

THRASH_NODES = np.array([], dtype=object)


class Nodes:
    def __init__(self, x, y, row, col, node_id):
        self.x, self.y = x, y  # row, col
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        self.parent_ptr = 0
        self.node_id = node_id

    def __str__(self):
        return f"Node at ({self.x}, {self.y}) - Row: {self.row}, Col: {self.col}"


@jit(nopython=True)
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


def is_obstacle_inside_room(room_coords, obstacles_coords):
    polygon = Polygon(room_coords)
    for obstacle_coords in obstacles_coords:
        obstacle_x, obstacle_y, width, height = obstacle_coords
        obstacle_points = [(obstacle_x, obstacle_y), (obstacle_x + width, obstacle_y),
                           (obstacle_x + width, obstacle_y + height), (obstacle_x, obstacle_y + height)]
        for point in obstacle_points:
            point_shapely = Point(point[0], point[1])
            if not polygon.contains(point_shapely):
                return False
    return True


def is_node_inside_room(point, room_coords):  # https://en.wikipedia.org/wiki/Point_in_polygon
    polygon = Polygon(room_coords)
    point = Point(point[0], point[1])
    return polygon.contains(point)


def is_node_inside_obstacle(node, obstacles_coords):
    node_x, node_y = node.x, node.y
    for obstacles_coord in obstacles_coords:
        obstacle_x, obstacle_y, width, height = obstacles_coord
        if obstacle_x <= node_x < obstacle_x + width and obstacle_y <= node_y < obstacle_y + height:
            np.append(THRASH_NODES, node)
            return True
    return False


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


def ant_colony(start_node, goal_node, grid):
    number_of_ants = 20
    number_of_iterations = 100
    decay_rate = 0.1
    alpha = 2
    beta = 2

    pheromone_levels = initialize_pheromones(grid)

    best_path = None
    best_path_length = float('inf')

    for iteration in range(number_of_iterations):
        print(f"ITERATION {iteration}")
        paths = []
        path_lengths = []

        for ant in range(number_of_ants):
            print(f"Ant {ant}")
            path, path_length = build_path(start_node, goal_node, grid, pheromone_levels, alpha, beta)
            paths.append(path)
            path_lengths.append(path_length)

            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length

        update_pheromones(pheromone_levels, paths, path_lengths, decay_rate)

    bp = [(node.x, node.y) for node in best_path]

    return bp


def initialize_pheromones(grid):
    pheromone_levels = {}
    for node in grid:
        if node.row != -1 and node.col != -1:
            for neighbor in node.neighbours_lst:
                pheromone_levels[(node, neighbor)] = 1.0  # Przykładowa inicjalizacja
    return pheromone_levels


def build_path(start_node, goal_node, grid, pheromone_levels, alpha, beta):
    current_node = start_node
    path = [current_node]
    path_length = 0

    while current_node != goal_node:
        next_node = choose_next_node(current_node, pheromone_levels, alpha, beta)
        path.append(next_node)
        path_length += ret_distance((current_node.x, current_node.y), (next_node.x, next_node.y))
        current_node = next_node

    return path, path_length


def choose_next_node(current_node, pheromone_levels, alpha, beta):
    probabilities = []
    total = 0

    for neighbor in current_node.neighbours_lst:
        pheromone = pheromone_levels[(current_node, neighbor)] ** alpha
        heuristic = (1 / ret_distance((current_node.x, current_node.y), (neighbor.x, neighbor.y))) ** beta
        probability = pheromone * heuristic
        probabilities.append((probability, neighbor))
        total += probability

    probabilities = [(prob / total, node) for prob, node in probabilities]
    next_node = random.choices([node for _, node in probabilities], weights=[prob for prob, _ in probabilities], k=1)[0]

    return next_node


def update_pheromones(pheromone_levels, paths, path_lengths, decay_rate):
    for path, path_length in zip(paths, path_lengths):
        for i in range(len(path) - 1):
            node, next_node = path[i], path[i + 1]
            pheromone_levels[(node, next_node)] += 1.0 / path_length

    for edge in pheromone_levels:
        pheromone_levels[edge] *= (1 - decay_rate)


def ui_runner(start_pt, goal_pt, grid, obstacles, room_coords, path):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
                              [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in room_coords], NODE_SIZE)

        pygame.display.update()

    pygame.quit()


def driver():
    start_time = time.time()

    start_point = (50, 50)
    goal_point = (550, 550)

    room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]

    # obstacles_coords = []
    obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500]]
    obstacles = get_obstacles(obstacles_coords)
    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        raise Exception("Obstacles outside of room!")

    grid = create_grid(obstacles_coords, room_coords)

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])

    sorted_thrash_set = sorted(THRASH_NODES, key=lambda node: (node.x, node.y))
    for item in sorted_thrash_set:
        print("Thrash node: {}".format(item))

    if start_node and goal_node:
        print("Starting ACO")
        ret_path = ant_colony(start_node=start_node, goal_node=goal_node, grid=grid)
    else:
        raise Exception("Nodes don't found!")

    if ret_path:
        print("Path found.")
        print(ret_path)
        print("Path length = ", len(ret_path))
    else:
        print("Path not found!")
        print(ret_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania algorytmu: {execution_time} sekundy")
    ui_runner(start_point, goal_point, grid, obstacles, room_coords, ret_path)


if __name__ == "__main__":
    start_time = time.time()
    print("Start")
    driver()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")
