from multiprocessing import Pool, cpu_count
from time import time

def factorize(number: int):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

if __name__ == '__main__':

    numbers = (128, 255, 99999, 10651060)
    start_time = time()
    with Pool(processes=cpu_count()) as pool:
        print(pool.map(factorize, numbers))
        pool.close()
        pool.join()
    
    end_time = time() - start_time
    print(f'App ended. [{end_time:.1f}] seconds...')

