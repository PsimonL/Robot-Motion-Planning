import environment


def cross_product(X, Y, Z):
    x1, y1 = Z[0] - X[0], Z[1] - X[1]
    x2, y2 = Y[0] - X[0], Y[1] - X[1]
    return x1 * y2 - x2 * y1


def between(X, Y, Z):
    return min(X[0], Y[0]) <= Z[0] <= max(X[0], Y[0]) and min(X[1], Y[1]) <= Z[1] <= max(X[1], Y[1])


# TODO: refactor for "room" attribute cause no longer exists
# def check_pair(pair1, pair2):
#     p_x1, p_y1 = pair1
#     p_x2, p_y2 = pair2
#
#     A, B = pair1, pair2
#
#     obj = environment.RobotSimulation()
#     for i in range(len(obj.room) - 1):
#         C, D = obj.room[i], obj.room[i + 1]
#         v1 = cross_product(C, D, A)
#         v2 = cross_product(C, D, B)
#         v3 = cross_product(A, B, C)
#         v4 = cross_product(A, B, D)
#
#         if (v1 > 0 and v2 < 0 or v1 < 0 and v2 > 0) and (v3 > 0 and v4 < 0 or v3 < 0 and v4 > 0):
#             return True
#
#         if v1 == 0 and between(C, D, A):
#             return True
#         if v2 == 0 and between(C, D, B):
#             return True
#         if v3 == 0 and between(A, B, C):
#             return True
#         if v4 == 0 and between(A, B, D):
#             return True
#         return False


def check_collision(rect1, rect2):
    x1, y1, width1, height1 = rect1.x, rect1.y, rect1.width, rect1.height
    x2, y2, width2, height2 = rect2.x, rect2.y, rect2.width, rect2.height

    if x1 < x2 + width2 and x1 + width1 > x2 and y1 < y2 + height2 and y1 + height1 > y2:
        return True
    else:
        return False