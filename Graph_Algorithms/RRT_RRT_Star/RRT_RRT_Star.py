import time

from RRTNodes import RRTNode
from Graph_Algorithms.GeometryUtils import get_obstacles, is_obstacle_inside_room
from RRT_Pathfinding import rrt_algorithm
from RRT_StarPathfinding import rrt_star_algorithm
from UiUtils import rrt_ui_runner


def rrt_main(flag):
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
    path, rrt_tree = [], []
    if flag == "RRT":
        path, rrt_tree = rrt_algorithm(start_node, goal_node, obstacles_coords, )
    elif flag == "RRT*":
        path, rrt_tree = rrt_star_algorithm(start_node, goal_node, obstacles_coords)

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
    flag = "RRT"
    rrt_main(flag)
