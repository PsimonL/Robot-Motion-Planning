cdef int count_digits_in_loop_cython(str input_string):
    cdef int count = 0
    cdef int i, n = len(input_string)
    for i in range(n):
        if input_string[i].isdigit():
            count += 1
    return count