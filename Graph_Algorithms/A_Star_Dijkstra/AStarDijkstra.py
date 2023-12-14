import time
import networkx as nx
from scipy.spatial.distance import euclidean

from Graph_Algorithms.ConstVars import THRASH_NODES
from Graph_Algorithms.GeometryUtils import get_obstacles, is_obstacle_inside_room
from GridUtils import create_grid, find_nodes_by_coordinates
from Pathfinding import a_star, dijkstra
from UiUtils import ui_runner

def main(algorithm_choice):
    start_time = time.time()
    start_point = (25, 25)
    goal_point = (550, 160)
    # start_point = (50, 50)
    # goal_point = (550, 100)
    # start_point = (200, 10)
    # goal_point = (400, 40)

    # room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    # room_coords = [(0, 0), (350, 0), (350, 150), (600, 150), (600, 600), (0, 600)]
    room_coords = [(0, 0), (350, 0), (350, 150), (600, 150), (600, 300), (390, 300), (390, 390), (600, 390), (600, 600), (120, 600), (120, 480), (0, 480)]
    obstacles_coords = [[50, 1, 60, 420], [140, 50, 40, 549], [200, 1, 20, 550], [220, 521, 300, 30], [490, 420, 30, 120], [350, 210, 40, 300], [300, 100, 40, 90], [450, 151, 40, 100]]
    # obstacles_coords = [[250, 300, 340, 50]]
    # obstacles_coords = [[1, 30, 550, 50], [50, 120, 549, 50], [1, 200, 100, 50]]
    # obstacles_coords = []
    # obstacles_coords = [[250, 100, 90, 200]]
    # obstacles_coords = [[275, 1, 50, 300]]
    # obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500], [450, 100, 50, 499]]
    obstacles = get_obstacles(obstacles_coords)
    # print("obstacles  =  ", obstacles)

    if not is_obstacle_inside_room(room_coords, obstacles_coords):
        raise Exception("Obstacles outside of room!")

    # start_time = time.time()
    grid = create_grid(obstacles_coords, room_coords)

    # for node in grid:
    #     print(f"Node {node.node_id} at ({node.x}, {node.y}) - Row: {node.row}, Col: {node.col}")

    # end_time = time.time()
    # print("Single process ", end_time - start_time)

    start_node = find_nodes_by_coordinates(grid=grid, x=start_point[0], y=start_point[1])
    goal_node = find_nodes_by_coordinates(grid=grid, x=goal_point[0], y=goal_point[1])

    sorted_thrash_set = sorted(THRASH_NODES, key=lambda node: (node.x, node.y))
    for item in sorted_thrash_set:
        print("Thrash node: {}".format(item))

    ret_path = None
    if start_node and goal_node:
        ret_path = a_star(start_node, goal_node) if algorithm_choice == "A*" else dijkstra(start_node, goal_node) if algorithm_choice == "Dijkstra" else None
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
    ui_runner(start_point, goal_point, grid, obstacles, room_coords, ret_path, algorithm_choice)


if __name__ == "__main__":
    start_time = time.time()
    algorithm_choice = "A*"  # "Dijkstra"
    print(f"Start {algorithm_choice}")
    main(algorithm_choice)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")