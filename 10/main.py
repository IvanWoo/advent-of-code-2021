import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

OPEN_CLOSE = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

CORRUPTED_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

COMPLETE_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def find_first_illegal(chunk):
    stack = []
    for char in chunk:
        if char in OPEN_CLOSE:
            stack.append(OPEN_CLOSE[char])
        else:
            expected = stack.pop()
            if char != expected:
                return char
    return None


def get_autocomplete(chunk):
    stack = []
    for char in chunk:
        if char in OPEN_CLOSE:
            stack.append(OPEN_CLOSE[char])
        else:
            expected = stack.pop()
            if char != expected:
                raise ValueError(f"{char} != {expected}")
    return stack


def get_autocomplete_score(chunk):
    ac = get_autocomplete(chunk)
    score = 0
    for char in reversed(ac):
        score = score * 5 + COMPLETE_SCORE[char]
    return score


def q1():
    ans = 0
    for chunk in get_input():
        if illegal := find_first_illegal(chunk):
            ans += CORRUPTED_SCORE[illegal]
    return ans


def q2():
    scores = []
    for chunk in get_input():
        if find_first_illegal(chunk):
            continue
        scores.append(get_autocomplete_score(chunk))
    n = len(scores)
    return sorted(scores)[n // 2]


def main():
    print(q1())
    print(q2())
    assert q1() == 193275
    assert q2() == 2429644557


if __name__ == "__main__":
    main()
