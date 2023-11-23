import pygame
import numpy as np
import random
import math

# ... (poprzedni kod)

# Parametry algorytmu RTT
MAX_ITERATIONS = 10000
EXPANSION_DISTANCE = 20

import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from numba import cuda, jit
import numpy as np
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

THRASH_NODES = np.array([], dtype=object)


class RRTNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None


def distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)


def get_random_point():
    return RRTNode(random.uniform(0, INNER_WIDTH), random.uniform(0, INNER_HEIGHT))


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


def nearest_node(tree, point):
    min_dist = float('inf')
    nearest = None

    for node in tree:
        d = distance(node, point)
        if d < min_dist:
            min_dist = d
            nearest = node

    return nearest


def new_point(start, end, max_distance):
    d = distance(start, end)
    if d < max_distance:
        return end
    else:
        theta = math.atan2(end.y - start.y, end.x - start.x)
        return RRTNode(start.x + max_distance * math.cos(theta),
                       start.y + max_distance * math.sin(theta))
def rrt_algorithm(start, goal, obstacles_coords):
    tree = [start]

    for _ in range(MAX_ITERATIONS):
        random_point = get_random_point()
        nearest = nearest_node(tree, random_point)
        new_node = new_point(nearest, random_point, EXPANSION_DISTANCE)

        # Sprawdź czy nowy punkt jest dostępny (nie koliduje z przeszkodami)
        if not is_node_inside_obstacle(new_node, obstacles_coords):
            new_node.parent = nearest
            tree.append(new_node)

            # Sprawdź czy osiągnięto cel
            if distance(new_node, goal) < EXPANSION_DISTANCE:
                path = [goal]
                current = new_node
                while current.parent:
                    path.append(current.parent)
                    current = current.parent
                return path[::-1], tree  # Return both the path and the RRT tree

    return None, tree  # Return the RRT tree even if the path is not found


# def rrt_algorithm(start, goal, obstacles_coords):
#     tree = [start]
#
#     for _ in range(MAX_ITERATIONS):
#         random_point = get_random_point()
#         nearest = nearest_node(tree, random_point)
#         new_node = new_point(nearest, random_point, EXPANSION_DISTANCE)
#
#         # Sprawdź czy nowy punkt jest dostępny (nie koliduje z przeszkodami)
#         if not is_node_inside_obstacle(new_node, obstacles_coords):
#             new_node.parent = nearest
#             tree.append(new_node)
#
#             # Sprawdź czy osiągnięto cel
#             if distance(new_node, goal) < EXPANSION_DISTANCE:
#                 path = [goal]
#                 current = new_node
#                 while current.parent:
#                     path.append(current.parent)
#                     current = current.parent
#                 return path[::-1]
#
#     return None


def rrt_ui_runner(start_pt, goal_pt, obstacles, room_coords, path, rrt_tree):
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

        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE,
                             (obstacle[0] + ADJUST_VECTOR, obstacle[1] + ADJUST_VECTOR, obstacle[2], obstacle[3]))

        pygame.draw.circle(screen, YELLOW, (start_pt[0] + ADJUST_VECTOR, start_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)
        pygame.draw.circle(screen, GREEN, (goal_pt[0] + ADJUST_VECTOR, goal_pt[1] + ADJUST_VECTOR), NODE_SIZE * 8)

        pygame.draw.circle(screen, RED, (INNER_WIDTH + ADJUST_VECTOR, INNER_HEIGHT + ADJUST_VECTOR), NODE_SIZE * 10)

        for node in rrt_tree:
            pygame.draw.circle(screen, WHITE, (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)), NODE_SIZE)

            if node.parent:
                pygame.draw.line(screen, WHITE,
                                 (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)),
                                 (int(node.parent.x + ADJUST_VECTOR), int(node.parent.y + ADJUST_VECTOR)),
                                 NODE_SIZE // 2)

        if path:
            adjusted_path = [(node.x + ADJUST_VECTOR, node.y + ADJUST_VECTOR) for node in path]
            for i in range(1, len(adjusted_path)):
                pygame.draw.line(screen, RED, adjusted_path[i - 1], adjusted_path[i], NODE_SIZE * 4)

        for node in rrt_tree:
            if node.parent:
                pygame.draw.line(screen, WHITE,
                                 (int(node.x + ADJUST_VECTOR), int(node.y + ADJUST_VECTOR)),
                                 (int(node.parent.x + ADJUST_VECTOR), int(node.parent.y + ADJUST_VECTOR)),
                                 NODE_SIZE)

        if len(room_coords) > 1:
            pygame.draw.lines(screen, ORANGE, True,
                              [(x + ADJUST_VECTOR, y + ADJUST_VECTOR) for x, y in room_coords], NODE_SIZE)

        pygame.display.update()

    pygame.quit()




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


def get_obstacles(obstacles):
    obstacle_rects = []
    for obstacle in obstacles:
        if isinstance(obstacle[0], list):
            for sub_obstacle in obstacle:
                obstacle_rects.append(pygame.Rect(sub_obstacle[0], sub_obstacle[1], sub_obstacle[2], sub_obstacle[3]))
        else:
            obstacle_rects.append(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
    return obstacle_rects


def rrt_driver():
    start_point = (50, 50)
    goal_point = (550, 550)

    room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500]]
    obstacles = get_obstacles(obstacles_coords)

    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        raise Exception("Obstacles outside of room!")

    start_time = time.time()

    start_node = RRTNode(start_point[0], start_point[1])
    goal_node = RRTNode(goal_point[0], goal_point[1])

    path, rrt_tree = rrt_algorithm(start_node, goal_node, obstacles_coords)

    if path:
        print("Path found.")
        print([(node.x, node.y) for node in path])
    else:
        print("Path not found!")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania algorytmu: {execution_time} sekundy")
    rrt_ui_runner(start_point, goal_point, obstacles, room_coords, path, rrt_tree)


if __name__ == "__main__":
    rrt_driver()
