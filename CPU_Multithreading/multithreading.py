import multiprocessing
import time

N = 100000000


def count_numbers(start, end):
    count = 0
    for i in range(start, end + 1):
        count += 1
    return count


def worker1(result):
    result[0] = count_numbers(0, N // 4)


def worker2(result):
    result[0] = count_numbers((N // 4) + 1, N // 2)


def worker3(result):
    result[0] = count_numbers((N // 2) + 1, 3 * (N // 4))


def worker4(result):
    result[0] = count_numbers((3 * N // 4) + 1, N)


def multiple_processes():
    result1, result2, result3, result4 = multiprocessing.Array('i', 1), multiprocessing.Array('i',
                                                                                              1), multiprocessing.Array(
        'i', 1), multiprocessing.Array('i', 1)

    start_time = time.time()

    process1 = multiprocessing.Process(target=worker1, args=(result1,))
    process2 = multiprocessing.Process(target=worker2, args=(result2,))
    process3 = multiprocessing.Process(target=worker3, args=(result3,))
    process4 = multiprocessing.Process(target=worker4, args=(result4,))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    process1.join()
    process2.join()
    process3.join()
    process4.join()

    result = result1[0] + result2[0] + result3[0] + result4[0]

    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print(f"Suma z multipleProcesses(): {result}")
    print(f"Czas wykonania multipleProcesses(): {duration} ms")


def single_process():
    start_time = time.time()

    result = count_numbers(0, N)

    end_time = time.time()
    duration = (end_time - start_time) * 1000

    print(f"Suma z singleProcess(): {result}")
    print(f"Czas wykonania singleProcess(): {duration} ms")


if __name__ == "__main__":
    multiple_processes()
    single_process()
