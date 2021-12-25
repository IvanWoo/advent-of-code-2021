import fileinput
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    mapping = {".": 0, ">": 1, "v": 2}
    grid = []
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            grid.append([mapping[c] for c in line.strip()])
    return grid


def debug(grid):
    for row in grid:
        print("".join(["." if c == 0 else ">" if c == 1 else "v" for c in row]))


def run(grid, is_east=True):
    rows, cols = len(grid), len(grid[0])
    updated = 0
    next_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                continue
            elif grid[row][col] == 1:
                if is_east and grid[row][(col + 1) % cols] == 0:
                    next_grid[row][(col + 1) % cols] = 1
                    updated += 1
                else:
                    next_grid[row][col] = 1
            elif grid[row][col] == 2:
                if not is_east and grid[(row + 1) % rows][col] == 0:
                    next_grid[(row + 1) % rows][col] = 2
                    updated += 1
                else:
                    next_grid[row][col] = 2
    return updated, next_grid


def run_all(grid):
    changes = 0
    updated, grid = run(grid)
    changes += updated
    updated, grid = run(grid, is_east=False)
    changes += updated
    return changes, grid


def q1():
    grid = get_input()
    steps = 0
    while True:
        # debug(grid)
        updated, grid = run_all(grid)
        # print(updated)
        steps += 1
        if updated == 0:
            break
    return steps


def q2():
    pass


def main():
    print(q1())
    # print(q2())
    assert q1() == 432
    # assert q2() == 42


if __name__ == "__main__":
    main()
