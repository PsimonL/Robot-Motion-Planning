room = [(10, 10), (20, 10), (20, 20), (10, 20)]
path = [(11, 19), (15, 15), (18, 15), (18, 12), (15, 12)]


def cross_product(X, Y, Z):
    x1, y1 = Z[0] - X[0], Z[1] - X[1]
    x2, y2 = Y[0] - X[0], Y[1] - X[1]
    return x1 * y2 - x2 * y1


def between(X, Y, Z):
    return min(X[0], Y[0]) <= Z[0] <= max(X[0], Y[0]) and min(X[1], Y[1]) <= Z[1] <= max(X[1], Y[1])


def check_pair(pair1, pair2):
    p_x1, p_y1 = pair1
    p_x2, p_y2 = pair2
    print(f"(p_x1, p_y1) = ({p_x1}, {p_y1})")
    print(f"(p_x2, p_y2) = ({p_x2}, {p_y2})")
    print()

    A, B = pair1, pair2

    for i in range(len(room) - 1):
        C, D = room[i], room[i + 1]
        v1 = cross_product(C, D, A)
        v2 = cross_product(C, D, B)
        v3 = cross_product(A, B, C)
        v4 = cross_product(A, B, D)

        if (v1 > 0 and v2 < 0 or v1 < 0 and v2 > 0) and (v3 > 0 and v4 < 0 or v3 < 0 and v4 > 0):
            return True

        if v1 == 0 and between(C, D, A):
            return True
        if v2 == 0 and between(C, D, B):
            return True
        if v3 == 0 and between(A, B, C):
            return True
        if v4 == 0 and between(A, B, D):
            return True
        return False


def main():
    print("Źródło: http://informatyka.wroc.pl/node/455?page=0,2")
    for i in range(len(path) - 1):
        if check_pair(path[i], path[i + 1]):
            raise Exception(f"NOT good for line: from {path[i]} to {path[i + 1]}")
        else:
            print(f"All good for line: from {path[i]} to {path[i + 1]}")


if __name__ == '__main__':
    main()
