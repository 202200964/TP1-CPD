import multiprocessing
import time
import random

# Variável global para armazenar o maior número primo encontrado
max_prime_global = multiprocessing.Value('q', 1)
lock = multiprocessing.Lock()  # Lock para garantir a consistência dos dados

# Função para verificar a primalidade de um número
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Função para encontrar um número primo aleatório dentro de um intervalo
def find_random_prime(start, end, queue):
    for _ in range(1000):  # Tentar várias vezes para encontrar um primo aleatório
        n = random.randint(start, end)
        if is_prime(n):
            queue.put(n)
            return
    queue.put(None)  # Indicar que nenhum primo foi encontrado

# Função principal para encontrar o maior número primo possível usando processos
def find_max_prime_parallel(num_processes, timeout):
    current_max = 1
    step = 10000000000000000 # Tamanho inicial do passo
    start_time = time.time()

    while time.time() - start_time < timeout:
        queue = multiprocessing.Queue()
        processes = []
        for i in range(num_processes):
            start = current_max + 1
            end = start + step
            process = multiprocessing.Process(target=find_random_prime, args=(start, end, queue))
            processes.append(process)
            process.start()
            current_max = end

        for process in processes:
            process.join(timeout=timeout - (time.time() - start_time))

        # Atualizar a variável global com o maior número primo encontrado por este lote de processos
        global max_prime_global
        with lock:
            while not queue.empty():
                prime = queue.get()
                if prime is not None and prime > max_prime_global.value:
                    max_prime_global.value = prime

    return max_prime_global.value

if __name__ == '__main__':
    timeout = int(input("Informe o tempo máximo de execução em segundos: "))
    num_processes = int(input("Informe o número de processos desejados: "))

    start_time = time.time()
    max_prime = find_max_prime_parallel(num_processes, timeout)
    end_time = time.time()

    print("Largest prime found:", max_prime)
    print("Time taken:", end_time - start_time, "seconds")
    print("Algarismos: ",len(str(max_prime)))
