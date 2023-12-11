import time
import networkx as nx

from Graph_Algorithms.ConstVars import THRASH_NODES
from Graph_Algorithms.GeometryUtils import get_obstacles, is_obstacle_inside_room
from GridUtils import create_grid, find_nodes_by_coordinates
from Pathfinding import a_star, dijkstra
from UiUtils import ui_runner

def main(algorithm_choice):
    start_time = time.time()
    print("Start")
    start_point = (300, 50)
    goal_point = (550, 160)
    # start_point = (100, 10)
    # goal_point = (500, 10)

    # room_coords = [(0, 0), (600, 0), (600, 600), (0, 600)]
    room_coords = [(0, 0), (350, 0), (350, 150), (600, 150), (600, 600), (0, 600)]

    # obstacles_coords = [[250, 300, 340, 50]]
    # obstacles_coords = [[1, 30, 550, 50], [50, 120, 549, 50], [1, 200, 100, 50]]
    # obstacles_coords = []
    obstacles_coords = [[200, 200, 100, 100]]
    # obstacles_coords = [[100, 1, 50, 350], [200, 100, 50, 499], [350, 1, 50, 500]]
    obstacles = get_obstacles(obstacles_coords)
    print("obstacles  =  ", obstacles)

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
        print("Path found.")
        print(ret_path)
    else:
        print("Path not found!")
        print(ret_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania algorytmu: {execution_time} sekundy")
    ui_runner(start_point, goal_point, grid, obstacles, room_coords, ret_path, algorithm_choice)


if __name__ == "__main__":
    start_time = time.time()
    algorithm_choice = "A*"  # "Dijkstra"
    print("Start")
    main(algorithm_choice)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Czas wykonania: {execution_time} sekundy")