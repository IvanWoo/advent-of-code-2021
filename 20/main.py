import fileinput
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    algo, matrix = "".join(fileinput.input(files=(INPUT_FILE))).split("\n\n")
    algo = tuple([int(char == "#") for char in algo.strip()])
    matrix = np.array(
        [[int(char == "#") for char in line.strip()] for line in matrix.split("\n")]
    )
    return algo, matrix


kernel = np.power(2, np.arange(8, -1, -1).reshape((3, 3)))


def run(algo, matrix, pad_value):
    matrix = np.pad(matrix, 2, constant_values=(pad_value))
    n, m = matrix.shape
    new_m = np.zeros((n, m), dtype=int)
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            sub = matrix[i - 1 : i + 2, j - 1 : j + 2]
            product = sub * kernel
            new_m[i, j] = algo[product.sum()]

    # trim the padding off
    return new_m[1:-1, 1:-1]


def run_many(n):
    algo, matrix = get_input()
    is_flash = algo[0] == 1
    pad_value = 0
    for _ in range(n):
        matrix = run(algo, matrix, pad_value)
        if is_flash:
            pad_value ^= 1
    return matrix.sum()


def q1():
    return run_many(2)


def q2():
    return run_many(50)


def main():
    print(q1())
    print(q2())
    assert q1() == 5437
    assert q2() == 19340


if __name__ == "__main__":
    main()
