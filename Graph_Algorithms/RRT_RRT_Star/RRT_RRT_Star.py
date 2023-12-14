import time
import numpy as np
from scipy.spatial.distance import euclidean
from RRTNodes import RRTNode
from Graph_Algorithms.GeometryUtils import get_obstacles, is_obstacle_inside_room
from RRT_Pathfinding import rrt_algorithm
from RRT_StarPathfinding import rrt_star_algorithm
from UiUtils import rrt_ui_runner


def rrt_main(algorithm_choice):
    # start_point = (50, 100)
    # goal_point = (550, 100)
    #
    # room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    # obstacles_coords = []

    # room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    # obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500], [450, 100, 50, 499]]
    # start_point = (50, 50)
    # goal_point = (550, 100)
    start_point = (200, 10)
    goal_point = (400, 40)
    obstacles_coords = [[275, 1, 50, 300]]
    room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]

    obstacles = get_obstacles(obstacles_coords)

    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        raise Exception("Obstacles outside of room!")

    start_time = time.time()

    start_node = RRTNode(start_point[0], start_point[1])
    goal_node = RRTNode(goal_point[0], goal_point[1])
    ret_path, rrt_tree = None, None

    if start_node and goal_node:
        ret_path, rrt_tree = rrt_algorithm(start_node, goal_node, obstacles_coords) if algorithm_choice == "RRT" else rrt_star_algorithm(start_node, goal_node, obstacles_coords) if algorithm_choice == "RRT*" else None
        print("Number of nodes in tree = ", len(rrt_tree))
    else:
        raise Exception("Nodes don't found!")

    if ret_path:
        print(f"Path found. {len(ret_path)} elements")
        # print(ret_path)
        distance = sum(euclidean(ret_path[i], ret_path[i+1]) for i in range(len(ret_path) - 1))
        print(f"Total distance: {distance}")
    else:
        print("Path not found!")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Algorithm execution time: {execution_time} seconds")
    rrt_ui_runner(start_point, goal_point, obstacles, room_coords, ret_path, rrt_tree, algorithm_choice)


if __name__ == "__main__":
    start_time = time.time()
    algorithm_choice = "RRT"  # "RRT*"
    print(f"Start {algorithm_choice}")
    rrt_main(algorithm_choice)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")
