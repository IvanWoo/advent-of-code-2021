import fileinput
from pathlib import Path
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_grid(dots):
    max_x = max(d[0] for d in dots)
    max_y = max(d[1] for d in dots)
    grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for x, y in dots:
        grid[y, x] = 1
    return grid


def get_input():
    dots = []
    instructions = []
    is_dots = True
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            if line == "\n":
                is_dots = False
                continue
            if is_dots:
                dots.append(line.strip().split(","))
            else:
                instructions.append(line.strip().split(" ")[-1].split("="))
    dots = [tuple(map(int, dot)) for dot in dots]
    instructions = [(dir, int(pos)) for dir, pos in instructions]
    return get_grid(dots), instructions


def debug(grid):
    for row in grid:
        print("".join(["#" if x else "█" for x in row]))
    print("\n")


def pad(A, B):
    ya, xa = A.shape
    yb, xb = B.shape
    diff_y = ya - yb
    diff_x = xa - xb
    B = np.pad(B, ((diff_y, 0), (0, 0)))
    B = np.pad(B, ((0, 0), (diff_x, 0)))
    return B


def fold(grid, instruct):
    dir, pos = instruct
    direction = 0 if dir == "y" else 1
    if direction == 0:
        A, B = grid[:pos], grid[pos + 1 :]
    else:
        A, B = grid[:, :pos], grid[:, pos + 1 :]
    B = np.flip(B, direction)
    B = pad(A, B)
    res = B + A
    return res.clip(0, 1)


def q1():
    grid, instructions = get_input()
    product = fold(grid, instructions[0])
    # debug(product)
    return np.sum(product)


def q2():
    grid, instructions = get_input()
    for instruct in instructions:
        # print(instruct)
        # print(grid.shape)
        grid = fold(grid, instruct)
    debug(grid)
    return np.sum(grid)


def main():
    print(q1())
    print(q2())
    assert q1() == 775
    # REUPUPKR
    assert q2() == 102


if __name__ == "__main__":
    main()
