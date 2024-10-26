import timeit
import multiprocessing
from pathlib import Path


def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        return result, elapsed
    return wrapper


def get_factors(n):
    factors = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.append(i)
            if i != n // i:
                factors.append(n // i)
    return sorted(factors)


@timeit_decorator
def factorize_multi(*numbers):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(get_factors, numbers)
    return results


@timeit_decorator
def factorize_single(*numbers):
    return [get_factors(n) for n in numbers]

if __name__ == '__main__':
    numbers = [i for i in range(1, 1000)]
    single_results, single_time = factorize_single(*numbers)
    
    print(f"Single Thread Results: {single_results[:5]}... (Total: {len(single_results)})")
    print(f"Single Thread Time: {single_time:.6f} seconds")


    multi_results, multi_time = factorize_multi(*numbers)
    print(f"Multi Thread Results: {multi_results[:5]}... (Total: {len(multi_results)})")
    print(f"Multi Thread Time: {multi_time:.6f} seconds")
