import fileinput
from pathlib import Path
from itertools import product

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    grid = []
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            grid.append([int(c) for c in line.strip()])
    return grid


class Grid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

        self.seen = set()
        self.score = 0

    def __str__(self):
        res = ""
        for row in self.grid:
            res += "".join(map(str, row))
            res += "\n"
        return res

    def add(self, n):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] += n

    def add_one(self):
        self.add(1)

    def neighbors(self, r, c):
        for dr, dc in product([-1, 0, 1], repeat=2):
            if dr == 0 and dc == 0:
                continue
            rr = r + dr
            cc = c + dc
            if 0 <= rr < self.rows and 0 <= cc < self.cols:
                yield rr, cc

    def flash_one(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.seen:
                    continue
                if self.grid[r][c] > 9:
                    self.seen.add((r, c))
                    for nr, nc in self.neighbors(r, c):
                        self.grid[nr][nc] += 1

    def flash(self):
        self.seen = set()
        prev_seen = set()
        while True:
            self.flash_one()
            if self.seen == prev_seen:
                break
            prev_seen = self.seen.copy()

    def cool_down(self):
        for r, c in self.seen:
            self.score += 1
            self.grid[r][c] = 0

    def run(self):
        self.add_one()
        self.flash()
        self.cool_down()

    def is_all_flashed(self):
        return sum(sum(row) for row in self.grid) == 0


def q1():
    grid = Grid(get_input())

    for _ in range(100):
        # print(grid)
        grid.run()
    return grid.score


def q2():
    grid = Grid(get_input())
    steps = 0
    while not grid.is_all_flashed():
        # print(grid)
        grid.run()
        steps += 1
    return steps


def main():
    print(q1())
    print(q2())
    assert q1() == 1659
    assert q2() == 227


if __name__ == "__main__":
    main()
