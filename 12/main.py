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
    return name.islower()


def is_big(name):
    return name.isupper()


def run():
    routes = get_input()
    pathes = []

    def backtrack(pos, visited):
        if pos == "end":
            pathes.append(visited)
            return
        for next_pos in routes[pos]:
            count = sum(next_pos == p for p in visited)
            if is_small(next_pos) and count == 1:
                continue
            backtrack(next_pos, visited + [next_pos])

    backtrack("start", ["start"])
    return pathes


def run2():
    routes = get_input()
    pathes = set()

    def backtrack(pos, visited, exclude_small=None):
        if exclude_small in ["start", "end"]:
            return
        if pos == "end":
            pathes.add(tuple(visited))
            return
        for next_pos in routes[pos]:
            count = sum(next_pos == p for p in visited)
            if is_small(next_pos):
                if (next_pos == exclude_small and count < 2) or count < 1:
                    backtrack(next_pos, visited + [next_pos], exclude_small)
                    backtrack(next_pos, visited + [next_pos], exclude_small or next_pos)
            else:
                backtrack(next_pos, visited + [next_pos], exclude_small)

    backtrack("start", ["start"])
    return pathes


def debug(pathes):
    for p in pathes:
        print(",".join(p))


def q1():
    pathes = run()
    return len(pathes)


def q2():
    pathes = run2()
    # debug(pathes)
    return len(pathes)


def main():
    print(q1())
    print(q2())
    assert q1() == 4549
    assert q2() == 120535


if __name__ == "__main__":
    main()
