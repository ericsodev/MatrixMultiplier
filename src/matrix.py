from __future__ import annotations

import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from typing import Optional, List, Any, Union
import csv


def _is_valid_matrix(matrix: List[List[int]]) -> bool:
    cols = -1
    for row in matrix:
        if cols == -1:
            cols = len(row)
        else:
            if cols != len(row) or cols == 0:
                return False
    return True


def _dot_product(lst1: List[int], lst2: List[int]) -> Optional[int]:
    """
    Returns the dot product of two equal length lists of integers
    :param lst1: List of integers
    :param lst2: List of integers
    :return: Dot product of both lists, None if unequal lengths

    >>> a = [1,2,3]
    >>> b = [-1, 3, 5]
    >>> _dot_product(a, b)
    20
    """

    if len(lst1) == len(lst2) != 0:
        dot_product = 0
        for i, j in zip(lst1, lst2):
            dot_product += i * j

        return dot_product
    else:
        return None


def _dot_product_multithread(r: int, c: int, lst1: List[int],
                             lst2: List[int]) -> Optional[(int, int, int)]:
    """
    Returns the dot product of two equal length lists of integers
    :param lst1: List of integers
    :param lst2: List of integers
    :return: Dot product of both lists, None if unequal lengths

    >>> a = [1,2,3]
    >>> b = [-1, 3, 5]
    >>> _dot_product(a, b)
    20
    """

    if len(lst1) == len(lst2) != 0:
        dot_product = 0
        for i, j in zip(lst1, lst2):
            dot_product += i * j

        return (r, c, dot_product)
    else:
        return None


def _select_column(lst: List[List[Any]], col: int) -> Optional[List[Any]]:
    column = []
    for row in lst:
        if len(row) > col:
            column.append(row[col])
        else:
            return None
    return column


class Matrix:

    def __init__(self, value: Union[str, List[List[int]], None]) -> None:
        """
        :param csvStr: A CSV matrix string
        """
        self.rows = 0
        self.columns = 0
        self.matrix: List[List[int]] = []

        if isinstance(value, str):
            self.load_csv_matrix(value)

        elif _is_valid_matrix(value):
            self.matrix = value
            self.rows = len(value)
            self.columns = len(value[0])

    def load_csv_matrix(self, csvStr: str) -> None:
        """
        Reads a CSV string containing the matrix and sets it as the matrix
        instance variable
        :param csvStr:
        :return: None

        >>> a = "1,2,3/n4,5,6/n7,8,9"
        >>> test = Matrix(a)
        >>> test.matrix
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        """
        lines = csvStr.split('/n')
        matrix: List[List[int]] = [list(map(int, line.split(','))) for line in
                                   lines]

        if _is_valid_matrix(matrix):
            self.matrix = matrix
            self.rows = len(matrix)
            self.columns = len(matrix[0])

    def __mul__(self, other: Matrix) -> Optional[Matrix]:
        """
        Multi-threadedly multiply two matrices
        :param other: Second Matrix
        :return: Product of the matrices, None if matrices are invalid
        >>> a = Matrix("1,2,3/n4,5,6/n7,8,9")
        >>> b = Matrix("1,2,3/n4,5,6/n7,8,9")
        >>> (a*b).matrix
        [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        """
        if self.columns == other.rows != 0 and \
                self.rows > 0 and other.columns:
            arr = [[0 for _ in range(other.columns)] for _ in range(self.rows)]
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = []
                for i in range(self.rows):
                    for j in range(other.columns):
                        futures.append(
                            executor.submit(
                                _dot_product_multithread, r=i, c=j,
                                lst1=self.matrix[i],
                                lst2=_select_column(other.matrix, j)))
                print("Loaded Threads")
                for future in concurrent.futures.as_completed(futures):
                    r, c, v = future.result()
                    arr[r][c] = v
                    print(f"Loaded [{r}][{c}]")

            return Matrix(arr)
        return None

    def single_threaded_mul(self, other: Matrix) -> Optional[Matrix]:
        """
        Single-threadedly multiply two matrices
        :param other: Second Matrix
        :return: Product of the matrices, None if matrices are invalid
        >>> a = Matrix("1,2,3/n4,5,6/n7,8,9")
        >>> b = Matrix("1,2,3/n4,5,6/n7,8,9")
        >>> a.single_threaded_mul(b).matrix
        [[30, 36, 42], [66, 81, 96], [102, 126, 150]]
        """
        if self.columns == other.rows != 0 and \
                self.rows > 0 and other.columns > 0:
            new_matrix = []
            new_rows = self.rows
            new_cols = other.columns
            for r in range(new_rows):
                new_row = []
                for c in range(new_cols):
                    new_row.append(
                        _dot_product(self.matrix[r],
                                     _select_column(other.matrix, c)))
                new_matrix.append(new_row)

            return Matrix(new_matrix)
        return None
