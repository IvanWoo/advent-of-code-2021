import fileinput
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    routes = defaultdict(set)
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            u, v = line.strip().split("-")
            routes[u].add(v)
            routes[v].add(u)
    return routes


def is_small(name):
    return name[0].islower()


def run(is_q2):
    routes = get_input()
    pathes = []

    def backtrack(pos, visited, support_small_dup):
        if pos == "end":
            pathes.append(visited)
            return
        for next_pos in routes[pos]:
            new_support_small_dup = support_small_dup
            if is_small(next_pos):
                if next_pos in visited:
                    if support_small_dup and (next_pos not in ["start", "end"]):
                        new_support_small_dup = False
                    else:
                        continue
            backtrack(next_pos, visited + [next_pos], new_support_small_dup)

    backtrack("start", ["start"], is_q2)
    return pathes


def debug(pathes):
    for p in sorted(pathes):
        print(",".join(p))


def q1():
    pathes = run(False)
    return len(pathes)


def q2():
    pathes = run(True)
    # debug(pathes)
    return len(pathes)


def main():
    print(q1())
    print(q2())
    assert q1() == 4549
    assert q2() == 120535


if __name__ == "__main__":
    main()
