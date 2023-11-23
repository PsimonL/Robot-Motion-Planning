import random

from Graph_Algorithms.ConstVars import INNER_WIDTH, INNER_HEIGHT
from RRTNodes import RRTNode
from EuclideanDistanceUtils import euclidean_distance

def get_random_point():
    return RRTNode(random.uniform(0, INNER_WIDTH), random.uniform(0, INNER_HEIGHT))
def nearest_node(tree, point):
    min_dist = float('inf')
    nearest = None

    for node in tree:
        d = euclidean_distance(node, point)
        if d < min_dist:
            min_dist = d
            nearest = node

    return nearest