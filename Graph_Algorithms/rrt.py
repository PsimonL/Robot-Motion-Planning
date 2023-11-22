import matplotlib.pyplot as plt
import random
import math

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

class RRT:
    def __init__(self, start, goal, obstacles, step_size, max_iter):
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        self.obstacles = obstacles
        self.step_size = step_size
        self.max_iter = max_iter
        self.nodes = [self.start]

    def distance(self, node1, node2):
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    def random_sample(self):
        if random.random() < 0.5:
            return Node(random.uniform(0, 10), random.uniform(0, 10))
        else:
            return Node(self.goal.x, self.goal.y)

    def nearest_neighbor(self, sample):
        min_dist = float('inf')
        nearest_node = None

        for node in self.nodes:
            d = self.distance(node, sample)
            if d < min_dist:
                min_dist = d
                nearest_node = node

        return nearest_node

    def new_node(self, nearest_node, sample):
        d = self.distance(nearest_node, sample)
        if d <= self.step_size:
            return sample
        else:
            theta = math.atan2(sample.y - nearest_node.y, sample.x - nearest_node.x)
            return Node(nearest_node.x + self.step_size * math.cos(theta),
                        nearest_node.y + self.step_size * math.sin(theta))

    def is_collision_free(self, node1, node2):
        # Check for collision with obstacles
        for obstacle in self.obstacles:
            if obstacle[0] < node2.x < obstacle[2] and obstacle[1] < node2.y < obstacle[3]:
                return False
        return True

    def generate_rrt(self):
        for _ in range(self.max_iter):
            sample = self.random_sample()
            nearest_node = self.nearest_neighbor(sample)
            new_node = self.new_node(nearest_node, sample)

            if self.is_collision_free(nearest_node, new_node):
                new_node.parent = nearest_node
                self.nodes.append(new_node)

        # Connect the goal to the nearest point in the tree
        final_node = self.nearest_neighbor(self.goal)
        if self.is_collision_free(final_node, self.goal):
            self.goal.parent = final_node
            self.nodes.append(self.goal)

    def plot_rrt(self):
        for obstacle in self.obstacles:
            plt.Rectangle((obstacle[0], obstacle[1]), obstacle[2] - obstacle[0], obstacle[3] - obstacle[1], fill=True,
                          color='gray')
            plt.gca().add_patch(plt.Rectangle((obstacle[0], obstacle[1]), obstacle[2] - obstacle[0],
                                             obstacle[3] - obstacle[1], fill=True, color='gray'))

        for node in self.nodes:
            if node.parent:
                plt.plot([node.x, node.parent.x], [node.y, node.parent.y], color='blue')

        plt.plot([self.start.x], [self.start.y], marker='o', markersize=5, color='green')
        plt.plot([self.goal.x], [self.goal.y], marker='o', markersize=5, color='red')

        plt.title('Rapidly Exploring Random Trees (RRT)')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.show()

if __name__ == "__main__":
    start = (1, 1)
    goal = (9, 9)
    obstacles = [(3, 3, 5, 5), (7, 7, 8, 8)]
    step_size = 0.5
    max_iter = 500

    rrt = RRT(start, goal, obstacles, step_size, max_iter)
    rrt.generate_rrt()
    rrt.plot_rrt()
