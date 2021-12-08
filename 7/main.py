import fileinput
import math
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            return map(int, line.split(","))


def get_medians(data):
    n = len(data)
    if n % 2 == 0:
        return [data[n // 2 - 1], data[n // 2]]
    else:
        return [data[n // 2]]


def get_avgs(data):
    avg = sum(data) / len(data)
    return [math.floor(avg), math.ceil(avg)]


def linear_cost(data, pos):
    return sum([abs(x - pos) for x in data])


# calculate arithmetic sequence sum
def as_sum(n):
    return n * (n + 1) // 2


def non_linear_cost(data, pos):
    return sum([as_sum(abs(x - pos)) for x in data])


def get_cost(data, cost_func, pos_func):
    return min([cost_func(data, x) for x in pos_func(data)])


def q1():
    data = sorted(list(get_input()))
    cost = get_cost(data, linear_cost, get_medians)
    return cost


def q2():
    data = sorted(list(get_input()))
    cost = get_cost(data, non_linear_cost, get_avgs)
    return cost


def main():
    print(q1())
    print(q2())
    assert q1() == 352254
    assert q2() == 99053143


if __name__ == "__main__":
    main()
