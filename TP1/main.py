import time
import random
from multiprocessing import Process, Manager

def is_prime(n): #miller rabin
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for _ in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(5):
        a = random.randint(2, n - 2)
        if not check(a, s, d, n):
            return False
    return True

def find_next_prime(max_prime):
    print("bruh")

def find_max_prime(timeout, num_processes):
    manager = Manager()
    max_prime = manager.Value('i', 3)  # Shared integer value

    processes = []
    for _ in range(num_processes):
        process = Process(target=find_next_prime, args=(max_prime,))
        process.start()
        processes.append(process)

    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        pass

    for process in processes:
        process.terminate()

    end_time = time.monotonic()
    return max_prime.value, end_time - start_time

def next_number_with_one_more_digit(number):
    num_digits = len(str(number))
    next_number = int('1' + '0' * num_digits) + 1
    return next_number

if __name__ == '__main__':
    num_processes = int(input("Enter the number of processes to create: "))
    timeout = int(input("Enter the duration (in seconds) for the program to run: "))
    max_prime, runtime = find_max_prime(timeout, num_processes)
    print("Maximum prime found:", max_prime)
    print("Runtime:", runtime, "seconds")
