import fileinput
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    lines = [x.strip().split(" -> ") for x in fileinput.input(files=(INPUT_FILE))]
    starts = [tuple(map(int, start.split(","))) for start, _ in lines]
    ends = [tuple(map(int, end.split(","))) for _, end in lines]
    return starts, ends


def is_vertical(start, end):
    return start[0] == end[0]


def is_horizontal(start, end):
    return start[1] == end[1]


def min_max(x):
    return min(x), max(x)


def get_k(p1, p2):
    return (p1[1] - p2[1]) / (p1[0] - p2[0])


def get_points(start, end, include_diag):
    if is_vertical(start, end):
        min_y, max_y = min_max([start[1], end[1]])
        for y in range(min_y, max_y + 1):
            yield (start[0], y)
    elif is_horizontal(start, end):
        min_x, max_x = min_max([start[0], end[0]])
        for x in range(min_x, max_x + 1):
            yield (x, start[1])
    elif include_diag:
        k = get_k(start, end)
        min_x, max_x = min_max([start[0], end[0]])
        min_y, max_y = min_max([start[1], end[1]])
        if k > 0:
            for x, y in zip(range(min_x, max_x + 1), range(min_y, max_y + 1)):
                yield (x, y)
        else:
            for x, y in zip(range(min_x, max_x + 1), range(max_y, min_y - 1, -1)):
                yield (x, y)


def debug(grid):
    max_x, max_y = max(x for x, _ in grid), max(y for _, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid[x, y], end=" ")
        print()


def get_ans(grid):
    # debug(grid)
    return sum(1 for _, v in grid.items() if v > 1)


def run(include_diag):
    starts, ends = get_input()
    grid = defaultdict(int)
    for start, end in zip(starts, ends):
        for x, y in get_points(start, end, include_diag):
            grid[x, y] += 1
    return get_ans(grid)


def q1():
    return run(False)


def q2():
    return run(True)


def main():
    print(q1())
    print(q2())
    assert q1() == 7318
    assert q2() == 19939


if __name__ == "__main__":
    main()
