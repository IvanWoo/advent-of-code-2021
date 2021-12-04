import fileinput
from pathlib import Path
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    lines = [
        list(map(int, x.replace(",", " ").split()))
        for x in fileinput.input(files=(INPUT_FILE))
        if x != "\n"
    ]
    draws = lines.pop(0)
    boards = np.split(np.array(lines), len(lines) // 5)
    return draws, boards


def find(board, target):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == target:
                return x, y
    return None, None


def do_draw_one(draw, boards, marks):
    for i, board in enumerate(boards):
        x, y = find(board, draw)
        if x is not None:
            marks[i][x, y] = 1
    return marks


def is_win(mark):
    n = len(mark)
    return any(mark.sum(axis=0) == n) or any(mark.sum(axis=1) == n)


def get_score(draw, board, mark):
    s = np.sum(board * np.logical_not(mark))
    return draw * s


def run(first):
    draws, boards = get_input()
    x, y = len(boards[0]), len(boards[0][0])
    marks = [np.zeros(shape=(x, y), dtype=np.uint8) for _ in range(len(boards))]
    wins = [0] * len(boards)

    for draw in draws:
        marks = do_draw_one(draw, boards, marks)
        for i, mark in enumerate(marks):
            if is_win(mark):
                wins[i] = 1
                if first or sum(wins) == len(boards):
                    return get_score(draw, boards[i], mark)


def q1():
    return run(True)


def q2():
    return run(False)


def main():
    print(q1())
    print(q2())
    assert q1() == 46920
    assert q2() == 12635


if __name__ == "__main__":
    main()
