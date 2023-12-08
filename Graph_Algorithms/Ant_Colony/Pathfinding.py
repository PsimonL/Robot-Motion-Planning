from PheromoneUtils import initialize_pheromones, build_path, update_pheromones


def ant_colony(start_node, goal_node, grid):
    number_of_ants = 10
    number_of_iterations = 100
    decay_rate = 0.1
    alpha = 1
    beta = 5

    pheromone_levels = initialize_pheromones(grid)

    best_path = None
    best_path_length = float('inf')

    for iteration in range(number_of_iterations):
        print(f"ITERATION {iteration}")
        paths = []
        path_lengths = []

        for ant in range(number_of_ants):
            print(f"Ant {ant}")
            path, path_length = build_path(start_node, goal_node, grid, pheromone_levels, alpha, beta)
            paths.append(path)
            path_lengths.append(path_length)

            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length

        update_pheromones(pheromone_levels, paths, path_lengths, decay_rate)

    bp = [(node.x, node.y) for node in best_path]

    return bp
