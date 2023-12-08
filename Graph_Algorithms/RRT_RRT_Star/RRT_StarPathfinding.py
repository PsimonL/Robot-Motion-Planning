import math

from RRTNodes import RRTNode
from EuclideanDistanceUtils import euclidean_distance
from LocalConstVars import MAX_ITERATIONS, EXPANSION_DISTANCE
from Pathfinding import get_random_point
from Pathfinding import nearest_node
from Graph_Algorithms.GeometryUtils import is_node_inside_obstacle


def new_point(start, end, max_distance):
    d = euclidean_distance(start, end)
    if d < max_distance:
        return end, start.cost + d
    else:
        theta = math.atan2(end.y - start.y, end.x - start.x)
        new_node = RRTNode(start.x + max_distance * math.cos(theta), start.y + max_distance * math.sin(theta))
        new_node.cost = start.cost + max_distance
        return new_node, new_node.cost


def rrt_star_algorithm(start, goal, obstacles_coords):
    tree = [start]

    for i in range(MAX_ITERATIONS):
        print(i)
        random_point = get_random_point()
        nearest = nearest_node(tree, random_point)
        new_node, cost = new_point(nearest, random_point, EXPANSION_DISTANCE)

        if not is_node_inside_obstacle(new_node, obstacles_coords):
            new_node.parent = nearest
            new_node.cost = cost

            for node in tree:
                if euclidean_distance(new_node, node) < EXPANSION_DISTANCE and new_node.cost + euclidean_distance(new_node,
                                                                                                                  node) < node.cost:
                    node.parent = new_node
                    node.cost = new_node.cost + euclidean_distance(new_node, node)

            tree.append(new_node)

            if euclidean_distance(new_node, goal) < EXPANSION_DISTANCE:
                path = [goal]
                current = new_node
                while current.parent:
                    path.append(current.parent)
                    current = current.parent
                return path[::-1], tree

    return None, tree
