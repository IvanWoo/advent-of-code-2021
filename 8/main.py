import fileinput
from pathlib import Path
from collections import Counter

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

NUM_TO_STR = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

STR_TO_NUM = {v: k for k, v in NUM_TO_STR.items()}


def finger_print(pattern):
    total = []
    for v in pattern:
        total = [*total, *[c for c in v]]
    return Counter(total)


def debug():
    print(STR_TO_NUM)
    print(finger_print(NUM_TO_STR.values()))


def get_map(pattern):
    def find_by_len(pattern, n):
        for p in pattern:
            if len(p) == n:
                return set(p)

    def find_by_count(fp, n):
        for k, v in fp.items():
            if v == n:
                return set(k)

    def extract(s):
        return list(s)[0]

    cf = find_by_len(pattern, 2)
    bcdf = find_by_len(pattern, 4)
    acf = find_by_len(pattern, 3)
    abcdefg = find_by_len(pattern, 7)

    _fp = finger_print(pattern)
    # default finger print: Counter({'f': 9, 'a': 8, 'c': 8, 'g': 7, 'd': 7, 'b': 6, 'e': 4})
    f = find_by_count(_fp, 9)
    b = find_by_count(_fp, 6)
    e = find_by_count(_fp, 4)

    a = acf - cf
    c = cf - f
    bd = bcdf - cf
    d = bd - b
    g = abcdefg - a - bcdf - e

    ans = {extract(k): v for k, v in zip([a, b, c, d, e, f, g], "abcdefg")}
    return ans


def translate(map, s):
    return "".join([map[c] for c in s])


def get_input():
    patterns = []
    outs = []
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            pattern, out = line.split("|")
            patterns.append(pattern.split())
            outs.append(out.split())
    return patterns, outs


def q1():
    _, outs = get_input()
    res = 0
    for out in outs:
        res += sum([len(o) in (2, 4, 3, 7) for o in out])
    return res


def q2():
    patterns, outs = get_input()
    res = 0
    for pattern, out in zip(patterns, outs):
        _map = get_map(pattern)
        for i, o in enumerate(reversed(out)):
            num = STR_TO_NUM["".join(sorted(translate(_map, o)))]
            res += num * (10 ** i)
    return res


def main():
    # debug()
    print(q1())
    print(q2())
    assert q1() == 383
    assert q2() == 998900


if __name__ == "__main__":
    main()
