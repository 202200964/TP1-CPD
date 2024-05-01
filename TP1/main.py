import os
import time
import random
from multiprocessing import Process, Manager, Lock

def is_prime(n):  # Miller-Rabin
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

def worker(max_prime, lock):
    while True:
        with lock:
            start_number = max_prime.value * random.randint(2, 10)  # Começa a partir do último primo encontrado multiplicado por um fator aleatório
        current_number = start_number
        while True:
            if is_prime(current_number):
                with lock:
                    if current_number > max_prime.value:  # Verifica se o número primo encontrado é maior que o maior primo atual
                        max_prime.value = current_number  # Atualiza o maior primo encontrado se necessário
                        print("New max prime found by process", current_number, " - pid: ", os.getpid())
                break
            current_number += 1

def find_max_prime(timeout, num_processes):
    manager = Manager()
    max_prime = manager.Value('i', 3)
    lock = Lock()

    processes = []
    for i in range(num_processes):
        process = Process(target=worker, args=(max_prime, lock))
        process.start()
        processes.append(process)

    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        pass

    for process in processes:
        process.terminate()

    end_time = time.monotonic()
    return max_prime.value, end_time - start_time

if __name__ == '__main__':
    num_processes = int(input("Enter the number of processes to create: "))
    timeout = int(input("Enter the duration (in seconds) for the program to run: "))
    max_prime, runtime = find_max_prime(timeout, num_processes)
    max_prime_str = str(max_prime)
    num_digits = len(max_prime_str)
    print("Maximum prime found:", max_prime, " (", num_digits, ")")
    print("Runtime:", runtime, "seconds")
