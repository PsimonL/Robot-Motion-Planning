import multiprocessing
import threading
import time

N = 100000000


def count_numbers(start, end):
    count = 0
    for i in range(start, end + 1):
        count += 1
    return count


def worker1(result):
    result[0] = count_numbers(0, N // 2)


def worker2(result):
    result[0] = count_numbers(N // 2 + 1, N)


def multiple_threads():
    mid = N // 2
    result1, result2 = multiprocessing.Array('i', 1), multiprocessing.Array('i', 1)

    start_time = time.time()

    process1 = multiprocessing.Process(target=worker1, args=(result1,))
    process2 = multiprocessing.Process(target=worker2, args=(result2,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()

    result = result1[0] + result2[0]

    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print(f"Suma z multipleProcesses(): {result}")
    print(f"Czas wykonania multipleProcesses(): {duration} ms")


def single_thread():
    start_time = time.time()

    result = count_numbers(0, N)

    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print(f"Suma z singleThread(): {result}")
    print(f"Czas wykonania singleThread(): {duration} ms")


if __name__ == "__main__":
    multiple_threads()
    single_thread()
