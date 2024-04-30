import time
import random
from multiprocessing import Process, Queue


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


def find_next_prime(last_prime, new_prime_queue):
    next_prime = last_prime + 1
    while True:
        if is_prime(next_prime):
            new_prime_queue.put(next_prime)
            print(next_prime)
            return
        next_prime += 1


def find_max_prime(timeout):
    max_prime = 3
    last_prime = 3
    new_prime_queue = Queue()

    process1 = Process(target=find_next_prime, args=(last_prime, new_prime_queue))
    process2 = Process(target=find_next_prime, args=(next_number_with_one_more_digit(last_prime), new_prime_queue))

    process1.start()
    process2.start()

    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        if not new_prime_queue.empty():
            last_prime = new_prime_queue.get()
            max_prime = max(max_prime, last_prime)
            process2.terminate()
            process2 = Process(target=find_next_prime, args=(next_number_with_one_more_digit(last_prime), new_prime_queue))
            process2.start()

    process1.terminate()
    process2.terminate()

    end_time = time.monotonic()
    return max_prime, end_time - start_time


def next_number_with_one_more_digit(number):
    num_digits = len(str(number))
    next_number = int('1' + '0' * num_digits) + 1
    return next_number


if __name__ == '__main__':
    max_prime, runtime = find_max_prime(10)
    print("Maximum prime found:", max_prime)
    print("Runtime:", runtime, "seconds")