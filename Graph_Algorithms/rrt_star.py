import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0.0

def euclidean_distance(node1, node2):
    return np.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def nearest_node(tree, random_node):
    distances = [euclidean_distance(node, random_node) for node in tree]
    return tree[np.argmin(distances)]

def new_node(nearest, random_node, step_size):
    distance = euclidean_distance(nearest, random_node)
    if distance <= step_size:
        return random_node
    else:
        theta = np.arctan2(random_node.y - nearest.y, random_node.x - nearest.x)
        new_x = nearest.x + step_size * np.cos(theta)
        new_y = nearest.y + step_size * np.sin(theta)
        return Node(new_x, new_y)

def is_collision_free(obstacle_list, new_node):
    for obstacle in obstacle_list:
        distance = euclidean_distance(obstacle, new_node)
        if distance < 1.0:  # Assuming the radius of the robot is 1.0
            return False
    return True

def rrt_star(start, goal, obstacle_list, max_iter=1000, step_size=1.0):
    tree = [start]

    for _ in range(max_iter):
        random_node = Node(np.random.uniform(0, 10), np.random.uniform(0, 10))

        nearest = nearest_node(tree, random_node)
        new_node_ = new_node(nearest, random_node, step_size)

        if is_collision_free(obstacle_list, new_node_):
            near_nodes = [node for node in tree if euclidean_distance(node, new_node_) < 2 * step_size]
            parent = nearest
            cost = parent.cost + euclidean_distance(parent, new_node_)

            for near_node in near_nodes:
                if is_collision_free(obstacle_list, near_node) and near_node.cost + euclidean_distance(near_node, new_node_) < cost:
                    parent = near_node
                    cost = near_node.cost + euclidean_distance(near_node, new_node_)

            new_node_.parent = parent
            new_node_.cost = cost
            tree.append(new_node_)

    # Find the best path
    goal_node = nearest_node(tree, goal)
    path = []
    while goal_node:
        path.insert(0, (goal_node.x, goal_node.y))
        goal_node = goal_node.parent

    return path

def plot_rrt_star(path, obstacle_list):
    plt.figure()
    for obstacle in obstacle_list:
        circle = plt.Circle((obstacle.x, obstacle.y), 1.0, color='r', fill=False)
        plt.gca().add_patch(circle)

    for i in range(len(path) - 1):
        plt.plot([path[i][0], path[i + 1][0]], [path[i][1], path[i + 1][1]], 'b-')

    plt.plot(path[0][0], path[0][1], 'go')  # Start node
    plt.plot(path[-1][0], path[-1][1], 'ro')  # Goal node

    plt.title('RRT* Path Planning')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()

# Example usage
start_node = Node(1, 1)
goal_node = Node(9, 9)
obstacles = [Node(3, 3), Node(4, 4), Node(7, 7)]

path = rrt_star(start_node, goal_node, obstacles)
plot_rrt_star(path, obstacles)
