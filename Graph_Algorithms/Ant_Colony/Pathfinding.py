from PheromoneUtils import initialize_pheromones, build_path, update_pheromones

# NUMBER_OF_ANTS = 10
# NUMBER_OF_ITERATIONS = 1000
NUMBER_OF_ANTS = 10
NUMBER_OF_ITERATIONS = 2

DECAY_RATE = 0.1
ALPHA = 1
BETA = 5


def ant_colony(start_node, goal_node, grid):
    pheromone_levels = initialize_pheromones(grid)

    best_path = None
    best_path_length = float('inf')

    for iteration in range(NUMBER_OF_ITERATIONS):
        print(f"ITERATION {iteration}")
        paths = []
        path_lengths = []

        for ant in range(NUMBER_OF_ANTS):
            print(f"Ant {ant}")
            path, path_length = build_path(start_node, goal_node, grid, pheromone_levels, ALPHA, BETA)
            paths.append(path)
            path_lengths.append(path_length)

            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length

        update_pheromones(pheromone_levels, paths, path_lengths, DECAY_RATE)

    bp = [(node.x, node.y) for node in best_path]

    return bp
