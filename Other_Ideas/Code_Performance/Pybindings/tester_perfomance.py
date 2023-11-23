import timeit

def ret_distance(p1, p2):
    dx, dy = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    D, D2 = 5, 7
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

point1 = (1, 2)
point2 = (4, 6)

# Measure the execution time
execution_time = timeit.timeit(lambda: ret_distance(point1, point2), number=100000)

print(f"Distance: {ret_distance(point1, point2)}")
print(f"Time taken by function: {execution_time} seconds")
