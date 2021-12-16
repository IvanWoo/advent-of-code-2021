import fileinput
from pathlib import Path
from heapq import heappush, heappop
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    grid = []
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            grid.append([int(x) for x in line.strip()])
    return np.array(grid)


def neighbors(x, y, grid):
    rows, cols = len(grid), len(grid[0])
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xx = x + dx
        yy = y + dy
        if 0 <= xx < rows and 0 <= yy < cols:
            yield xx, yy


def shortest_path(grid, start, end):
    pq = []
    heappush(pq, (0, start))
    visited = set()
    while pq:
        cost, (x, y) = heappop(pq)
        if (x, y) == end:
            return cost
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for nx, ny in neighbors(x, y, grid):
            heappush(pq, (cost + grid[nx][ny], (nx, ny)))


def large(grid):
    row_stacks = [(grid + i - 1) % 9 + 1 for i in range(5)]
    grid = np.hstack(row_stacks)
    col_stacks = [(grid + i - 1) % 9 + 1 for i in range(5)]
    grid = np.vstack(col_stacks)
    return grid


def q1():
    grid = get_input()
    rows, cols = len(grid), len(grid[0])
    return shortest_path(grid, (0, 0), (rows - 1, cols - 1))


def q2():
    grid = get_input()
    grid = large(grid)
    rows, cols = len(grid), len(grid[0])
    return shortest_path(grid, (0, 0), (rows - 1, cols - 1))


def main():
    print(q1())
    print(q2())
    assert q1() == 595
    assert q2() == 2914


if __name__ == "__main__":
    main()
