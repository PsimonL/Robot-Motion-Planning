# #
# #
# # def f(x):
# #     return x*x
# #
# # if __name__ == '__main__':
# #     with Pool(5) as p:
# #         print(p.map(f, [1, 2, 3]))
#
#
# from multiprocessing import Process
# import os
#
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

import numpy as np
from timeit import default_timer as timer
import multiprocessing


# normal function to run on cpu
def func(a):
    for i in range(10000000):
        a[i] += 1


def func2(a):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        a = pool.map(lambda x: x + 1, a)
    return a


if __name__ == "__main__":
    n = 10000000
    a = np.ones(n, dtype=np.float64)

    start = timer()
    func(a)
    print("without multiprocessing:", timer() - start)

    start = timer()
    a = func2(a)
    print("with multiprocessing:", timer() - start)