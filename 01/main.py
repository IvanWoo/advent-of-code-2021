import fileinput
from pathlib import Path
from collections import deque

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield int(line)


def get_sliding_window_sum(iterable, size):
    window = deque(maxlen=size)
    for item in iterable:
        window.append(item)
        if len(window) == size:
            yield sum(window)


def increases(iterable):
    ans = 0
    prev = None
    for curr in iterable:
        if prev and curr > prev:
            ans += 1
        prev = curr
    return ans


def q1():
    return increases(get_input())


def q2():
    return increases(get_sliding_window_sum(get_input(), 3))


def main():
    print(q1())
    print(q2())
    assert q1() == 1226
    assert q2() == 1252


if __name__ == "__main__":
    main()
