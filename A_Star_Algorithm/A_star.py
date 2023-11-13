import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from numba import cuda, jit
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

# NUM_ROWS = ((INNER_WIDTH) // 100) + 1
# NUM_COLS = ((INNER_HEIGHT) // 100) + 1
NUM_ROWS = ((INNER_WIDTH) // 5) + 1
NUM_COLS = ((INNER_HEIGHT) // 5) + 1
# NUM_ROWS = INNER_WIDTH
# NUM_COLS = INNER_HEIGHT

THRASH_NODES = set()


# class Environment:
#     def __init__(self):


class Nodes:
    def __init__(self, x, y, row, col, node_id):
        self.x, self.y = x, y  # row, col
        self.row, self.col = row, col  # multiple of 5, distance on diangonals will be 7 and horizontal as well as vertical would be 5
        self.G, self.H = 0, 0  # G - distance from current node to start node , H - heuristic distance from current node to end node
        self.F = self.G + self.H  # F (node in nodes) = G (node in nodes) + H (node in nodes)
        self.parent_ptr = 0
        self.node_id = node_id
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
            THRASH_NODES.add(node)
            return True
    return False


def create_grid(obstacles_coords, room_coords) -> list:
    grid = []
    nodes_id = 1
    nodes_outside_room = 1
    to_remove = []

    for row in range(1, NUM_ROWS - 1):
        for col in range(1, NUM_COLS - 1):
            # x = col * 100
            # y = row * 100
            x = col * 5
            y = row * 5
            # x = col
            # y = row
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
                to_remove.append(node)
                # print(f"DELETED Node {node.node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")

    set_neighbours(grid, obstacles_coords)

    for thrash_node in to_remove:
        grid.remove(thrash_node)

    print(f"Grid set. {nodes_id - nodes_outside_room} nodes.")
    print("Neighbours set.")
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


if __name__ == "__main__":
    # start_point = (300, 200)
    # goal_point = (300, 500)
    start_point = (100, 100)
    goal_point = (400, 400)
    # start_point = (100, 10)
    # goal_point = (500, 10)

    room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    # room_coords = [(0, 0), (350, 0), (350, 150), (600, 150), (600, 600), (0, 600)]

    # obstacles_coords = [[0, 100, 400, 50], [0, 400, 200, 100], [50, 220, 600, 50]]
    # obstacles_coords = [[250, 300, 340, 50]]
    # obstacles_coords = [[1, 30, 550, 50], [50, 120, 549, 50], [1, 200, 100, 50]]
    obstacles_coords = []
    obstacles = get_obstacles(obstacles_coords)

    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        # raise RuntimeError("")
        raise Exception("Obstacles outside of room!")

    start_time = time.time()
    grid = create_grid(obstacles_coords, room_coords)

    end_time = time.time()
    print("Single process ", end_time - start_time)


    # for node in grid:
    #     print(f"Node {node.node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")

    # sorted_thrash_set = sorted(THRASH_NODES, key=lambda node: (node.x, node.y))
    # for item in sorted_thrash_set:
    #     print("Thrash node: {}".format(item))

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])

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
