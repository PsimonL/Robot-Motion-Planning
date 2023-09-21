#include <iostream>
#include <thread>
#include <chrono>

const int N = 100000000;

int countNumbers(int start, int end) {
    int count = 0;
    for (int i = start; i <= end; ++i) {
        count += 1;
    }
    return count;
}

void multipleThreads() {
    int mid = N / 2;
    int result1, result2;

    auto start_time = std::chrono::high_resolution_clock::now();

    std::thread thread1([&result1](){ result1 = countNumbers(0, N / 2); });
    std::thread thread2([&result2](){ result2 = countNumbers(N / 2 + 1, N); });

    thread1.join();
    thread2.join();

    int result = result1 + result2;

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Suma z multipleThreads(): " << result << std::endl;
    std::cout << "Czas wykonania multipleThreads(): " << duration << " ms" << std::endl;
}

void singleThread() {
    auto start_time = std::chrono::high_resolution_clock::now();

    int result = countNumbers(0, N);

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();

    std::cout << "Suma z singleThread(): " << result << std::endl;
    std::cout << "Czas wykonania singleThread(): " << duration << " ms" << std::endl;
}

int main() {
    multipleThreads();
    singleThread();
    return 0;
}
