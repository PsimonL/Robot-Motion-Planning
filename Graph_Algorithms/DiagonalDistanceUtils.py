from numba import cuda, jit

@jit(nopython=True)
def diagonal_distance(p1: tuple, p2: tuple) -> int:  # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
    dx, dy = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    D, D2 = 5, 7  # cost 5 for horizontal and vertical, cost 7 for diagonal
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)  # Diagonal Distance