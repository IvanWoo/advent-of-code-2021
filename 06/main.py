import fileinput
from os import umask
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    lines = [line.strip() for line in fileinput.input(files=INPUT_FILE)]
    return map(int, lines[0].split(","))


def spawn(fishes):
    new_fishes = defaultdict(int)
    new_fishes[8] = fishes[0]
    new_fishes[6] = fishes[0]
    for i in range(8):
        new_fishes[i] += fishes[i + 1]
    return new_fishes


def init_fishes():
    fishes = defaultdict(int)
    for day in get_input():
        fishes[day] += 1
    return fishes


def run(n):
    fishes = init_fishes()
    for _ in range(n):
        fishes = spawn(fishes)
    return sum(fishes.values())


def q1():
    return run(80)


def q2():
    return run(256)


def main():
    print(q1())
    print(q2())
    assert q1() == 377263
    assert q2() == 1695929023803


if __name__ == "__main__":
    main()
