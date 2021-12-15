import fileinput
from pathlib import Path
from collections import Counter, defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    template = ""
    rules = dict()
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            if not template:
                template = line.strip()
                continue
            if line == "\n":
                continue
            input, output = line.strip().split(" -> ")
            rules[input] = output
    return template, rules


def step(counts, rules):
    result = defaultdict(int)
    for (a, b), n in counts.items():
        if c := rules.get(a + b):
            result[a + c] += n
            result[c + b] += n
        else:
            result[a + b] += n
    return result


def result(template, counts):
    result = defaultdict(int)
    for (a, b), n in counts.items():
        result[a] += n
        result[b] += n

    # only the first and last are not double counted
    first, last = template[0], template[-1]
    result[first] += 1
    result[last] += 1
    v = result.values()
    return (max(v) - min(v)) // 2


def q1():
    template, rules = get_input()
    counts = Counter(a + b for a, b in zip(template, template[1:]))
    for _ in range(10):
        counts = step(counts, rules)
    return result(template, counts)


def q2():
    template, rules = get_input()
    counts = Counter(a + b for a, b in zip(template, template[1:]))
    for _ in range(40):
        counts = step(counts, rules)
    return result(template, counts)


def main():
    print(q1())
    print(q2())
    assert q1() == 2988
    assert q2() == 3572761917024


if __name__ == "__main__":
    main()
