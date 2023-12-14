import time
import random
import multiprocessing
from scipy.spatial.distance import euclidean


from Graph_Algorithms.ConstVars import THRASH_NODES
from Graph_Algorithms.GeometryUtils import get_obstacles, is_obstacle_inside_room
from GridUtils import create_grid, find_nodes_by_coordinates
from Pathfinding import ant_colony
from UiUtils import ui_runner

def driver():
    start_time = time.time()

    start_point = (50, 50)
    goal_point = (550, 100)

    room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]

    # obstacles_coords = []
    obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500], [450, 100, 50, 499]]
    obstacles = get_obstacles(obstacles_coords)
    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        raise Exception("Obstacles outside of room!")

    grid = create_grid(obstacles_coords, room_coords)

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])

    sorted_thrash_set = sorted(THRASH_NODES, key=lambda node: (node.x, node.y))
    for item in sorted_thrash_set:
        print("Thrash node: {}".format(item))

    ret_path = None
    if start_node and goal_node:
        ret_path = ant_colony(start_node=start_node, goal_node=goal_node, grid=grid)
    else:
        raise Exception("Nodes don't found!")

    if ret_path:
        print(f"Path found. {len(ret_path)} elements")
        print(ret_path)
        distance = sum(euclidean(ret_path[i], ret_path[i+1]) for i in range(len(ret_path) - 1))
        print(f"Total distance: {distance}")
    else:
        print("Path not found!")
        print(ret_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Algorithm execution time: {execution_time} seconds")
    ui_runner(start_point, goal_point, grid, obstacles, room_coords, ret_path)


if __name__ == "__main__":
    start_time = time.time()
    print("Start ACO")
    driver()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")