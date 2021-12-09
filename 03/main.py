import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield int(line, 2)


def split(values, index):
    mask = 1 << index
    zeros = []
    ones = []
    for value in values:
        if value & mask:
            ones.append(value)
        else:
            zeros.append(value)
    return zeros, ones


def q1():
    values = list(get_input())

    gamma = 0
    epsilon = 0
    for i in range(12):
        zeros, ones = split(values, i)
        if len(ones) > len(zeros):
            gamma |= 1 << i
        else:
            epsilon |= 1 << i
    return gamma * epsilon


def search(values, less):
    for i in range(11, -1, -1):
        zeros, ones = split(values, i)
        if less:
            if len(ones) < len(zeros):
                values = ones
            else:
                values = zeros
        else:
            if len(ones) >= len(zeros):
                values = ones
            else:
                values = zeros
        if len(values) == 1:
            return values[0]


def q2():
    values = list(get_input())
    return search(values, 0) * search(values, 1)


def main():
    print(q1())
    print(q2())
    assert q1() == 3847100
    assert q2() == 4105235


if __name__ == "__main__":
    main()
