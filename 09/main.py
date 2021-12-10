import fileinput
from pathlib import Path
from functools import reduce

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    res = []
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            res.append([int(n) for n in line.strip()])
    return res


def neighbors(x, y, grid):
    rows, cols = len(grid), len(grid[0])
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xx = x + dx
        yy = y + dy
        if 0 <= xx < rows and 0 <= yy < cols:
            yield xx, yy


def bfs(grid, visited, start):
    count = 0
    queue = [start]
    while queue:
        x, y = queue.pop(0)
        if visited[x][y]:
            continue
        visited[x][y] = True
        if grid[x][y] == 9:
            continue
        count += 1
        queue.extend(neighbors(x, y, grid))
    return count


def q1():
    grid = get_input()
    res = 0
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if all(grid[r][c] < grid[nr][nc] for nr, nc in neighbors(r, c, grid)):
                res += grid[r][c] + 1
    return res


def q2():
    grid = get_input()
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    counts = []
    for r in range(rows):
        for c in range(cols):
            if count := bfs(grid, visited, (r, c)):
                counts.append(count)
    return reduce(lambda a, b: a * b, sorted(counts)[-3:])


def main():
    print(q1())
    print(q2())
    assert q1() == 448
    assert q2() == 1417248


if __name__ == "__main__":
    main()
