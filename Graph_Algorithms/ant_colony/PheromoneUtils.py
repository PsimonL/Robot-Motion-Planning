import random

from Graph_Algorithms.DiagonalDistanceUtils import diagonal_distance


def initialize_pheromones(grid):
    pheromone_levels = {}
    for node in grid:
        if node.row != -1 and node.col != -1:
            for neighbor in node.neighbours_lst:
                pheromone_levels[(node, neighbor)] = 1.0  # Przykładowa inicjalizacja
    return pheromone_levels


def build_path(start_node, goal_node, grid, pheromone_levels, alpha, beta):
    current_node = start_node
    path = [current_node]
    path_length = 0

    while current_node != goal_node:
        next_node = choose_next_node(current_node, pheromone_levels, alpha, beta)
        path.append(next_node)
        path_length += diagonal_distance((current_node.x, current_node.y), (next_node.x, next_node.y))
        current_node = next_node

    return path, path_length


def choose_next_node(current_node, pheromone_levels, alpha, beta):
    probabilities = []
    total = 0

    for neighbor in current_node.neighbours_lst:
        pheromone = pheromone_levels[(current_node, neighbor)] ** alpha
        heuristic = (1 / diagonal_distance((current_node.x, current_node.y), (neighbor.x, neighbor.y))) ** beta
        probability = pheromone * heuristic
        probabilities.append((probability, neighbor))
        total += probability

    probabilities = [(prob / total, node) for prob, node in probabilities]
    next_node = random.choices([node for _, node in probabilities], weights=[prob for prob, _ in probabilities], k=1)[0]

    return next_node


def update_pheromones(pheromone_levels, paths, path_lengths, decay_rate):
    for path, path_length in zip(paths, path_lengths):
        for i in range(len(path) - 1):
            node, next_node = path[i], path[i + 1]
            pheromone_levels[(node, next_node)] += 1.0 / path_length

    for edge in pheromone_levels:
        pheromone_levels[edge] *= (1 - decay_rate)
