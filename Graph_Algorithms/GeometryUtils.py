import pygame
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import numpy as np
from Graph_Algorithms.ConstVars import THRASH_NODES

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
            np.append(THRASH_NODES, node)
            return True
    return False