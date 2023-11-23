from Graph_Algorithms.DiagonalDistanceUtils import diagonal_distance


def a_star_dijkstra(start, goal, algorithm_choice):  # https://en.wikipedia.org/wiki/A*_search_algorithm
    open_set = []
    close_set = []

    open_set.append(start)
    while len(open_set) > 0:
        current_node = open_set[0]
        for node in open_set:
            if node.F < current_node.F or node.F == current_node.F and node.H < current_node.H:
                current_node = node

        if current_node == goal:
            path = []
            while current_node is not None:
                if isinstance(current_node, int):
                    break
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent_ptr
            return path[::-1]

        close_set.append(current_node)
        open_set.remove(current_node)

        for neighbor in current_node.neighbours_lst:
            if neighbor in close_set:
                continue

            tentative_g_score = current_node.G + diagonal_distance((current_node.x, current_node.y),
                                                                   (neighbor.x, neighbor.y))
            neighbor.parent_ptr = current_node
            neighbor.G = tentative_g_score

            # if True, means A* and heuristic distance from current to finish,
            # elif False means Dijkstra was picked and neighbor.H = 0
            if algorithm_choice:
                neighbor.H = diagonal_distance((neighbor.x, neighbor.y), (goal.x, goal.y))

            # So if False means neighbor.F = neighbor.G + 0 => neighbor.F = neighbor.G
            neighbor.F = neighbor.G + neighbor.H

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= neighbor.G:
                continue
    return None
