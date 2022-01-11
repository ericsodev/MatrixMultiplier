import timeit
from typing import List, Optional
import random
from timeit import default_timer
from matrix import Matrix


def generate_random_matrix(rows: Optional[int], cols: Optional[int]) -> List[List[int]]:
    r = random.Random()
    r.seed(1808)
    if not rows:
        rows = r.randint(300, 601)
    if not cols:
        cols = r.randint(300, 601)

    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(r.randint(-10000, 10001))
        matrix.append(row)

    return matrix


if __name__ == '__main__':
    matrix1 = generate_random_matrix(None, None)
    matrix2 = generate_random_matrix(len(matrix1[0]), None)
    print('Matrices, created')

    # Test for single threaded approach
    # start = timeit.default_timer()
    # result1 = Matrix(matrix1).single_threaded_mul(Matrix(matrix2)).matrix
    # end = timeit.default_timer()
    # print(f'Results for single-threaded: {str(end - start + 1)} secs')

    # Test for multi-threaded approach
    start = timeit.default_timer()
    result2 = (Matrix(matrix1) * Matrix(matrix2)).matrix
    end = timeit.default_timer()
    print(f'Results for multi-threaded: {str(end - start + 1)} secs')

    # print(f"Equal?: {result1==result2}")
