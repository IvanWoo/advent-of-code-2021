import fileinput
from pathlib import Path
from itertools import cycle, product
from functools import lru_cache
from collections import Counter

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    return [int(line.strip()[-1]) for line in fileinput.input(files=(INPUT_FILE))]


def deterministic_dice():
    yield from cycle(range(1, 101))


def run():
    poses = get_input()
    scores = [0, 0]
    turn = 0
    dice = deterministic_dice()
    while True:
        who = turn % 2
        turn += 1
        poses[who] = (poses[who] + next(dice) + next(dice) + next(dice) - 1) % 10 + 1
        scores[who] += poses[who]

        if scores[who] >= 1000:
            break
    return min(scores) * turn * 3


def q1():
    return run()


def quantum_dice():
    c = Counter([sum(x) for x in product([1, 2, 3], repeat=3)])
    return [(k, v) for k, v in c.items()]


@lru_cache(maxsize=None)
def solve(who, player0, player1, score0, score1):
    players = [player0, player1]
    scores = [score0, score1]

    if scores[0] >= 21:
        return (1, 0)
    if scores[1] >= 21:
        return (0, 1)

    ans = [0, 0]

    dice = quantum_dice()
    for roll in dice:
        add, ways = roll
        new_players = players[:]
        new_scores = scores[:]
        new_players[who] = (new_players[who] + add - 1) % 10 + 1
        new_scores[who] += new_players[who]
        now = solve(
            who ^ 1, new_players[0], new_players[1], new_scores[0], new_scores[1]
        )
        ans[0] += now[0] * ways
        ans[1] += now[1] * ways

    return ans


def q2():
    palyers = get_input()
    return max(solve(0, palyers[0], palyers[1], 0, 0))


def main():
    print(q1())
    print(q2())
    assert q1() == 989352
    assert q2() == 430229563871565


if __name__ == "__main__":
    main()
