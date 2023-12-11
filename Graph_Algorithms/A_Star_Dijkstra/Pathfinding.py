from Graph_Algorithms.DistanceUtils import diagonal_distance, heuristic
import networkx as nx
from math import sqrt


# def a_star_dijkstra(graph, start, goal):
#     path = nx.astar_path(graph, start, goal, heuristic=diagonal_distance)
#     return path

def a_star(start, goal):
    open_set = []
    close_set = []

    start.G = 0
    start.H = diagonal_distance((start.x, start.y), (goal.x, goal.y))
    start.F = start.G + start.H
    open_set.append(start)

    while open_set:
        current_node = open_set[0]
        for node in open_set:
            if node.F < current_node.F or (node.F == current_node.F and node.H < current_node.H):
                current_node = node

        if current_node == goal:
            path = []
            while current_node is not None:
                if isinstance(current_node, int):
                    break
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent_ptr
            return path[::-1]

        open_set.remove(current_node)
        close_set.append(current_node)

        for neighbor in current_node.neighbours_lst:
            if neighbor in close_set:
                continue

            tentative_g_score = current_node.G + diagonal_distance((current_node.x, current_node.y),
                                                                   (neighbor.x, neighbor.y))

            if neighbor not in open_set or tentative_g_score < neighbor.G:
                neighbor.parent_ptr = current_node
                neighbor.G = tentative_g_score
                neighbor.H = diagonal_distance((neighbor.x, neighbor.y), (goal.x, goal.y))
                neighbor.F = neighbor.G + neighbor.H

                if neighbor not in open_set:
                    open_set.append(neighbor)
    return None


def dijkstra(start, goal):
    open_set = []
    close_set = []

    start.G = 0
    open_set.append(start)

    while open_set:
        current_node = open_set[0]
        for node in open_set:
            if node.G < current_node.G:
                current_node = node

        if current_node == goal:
            path = []
            while current_node is not None:
                if isinstance(current_node, int):
                    break
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent_ptr
            return path[::-1]

        open_set.remove(current_node)
        close_set.append(current_node)

        for neighbor in current_node.neighbours_lst:
            if neighbor in close_set:
                continue

            tentative_g_score = current_node.G + diagonal_distance((current_node.x, current_node.y),
                                                           (neighbor.x, neighbor.y))

            if neighbor not in open_set or tentative_g_score < neighbor.G:
                neighbor.parent_ptr = current_node
                neighbor.G = tentative_g_score

                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None