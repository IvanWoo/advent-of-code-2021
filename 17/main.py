import fileinput
from pathlib import Path
from functools import cache

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def parse(range_str):
    """
    range_str: y=123..456
    returns (123, 456)
    """
    return [int(r) for r in range_str.strip().split("=")[1].strip().split("..")]


@cache
def get_input():
    line = list(fileinput.input(files=(INPUT_FILE)))[0]
    x_range, y_range = line.split(":")[1].strip().split(",")
    xs, ys = parse(x_range), parse(y_range)
    return xs, ys


class Probe:
    def __init__(self, vx, vy) -> None:
        self.x = 0
        self.y = 0
        self.vx = vx
        self.vy = vy
        self.xs, self.ys = get_input()

        self.history = []

    def __repr__(self):
        return f"<Probe pos=({self.x}, {self.y}), speed=({self.vx}, {self.vy})>"

    def is_in_range(self, x, y):
        return self.xs[0] <= x <= self.xs[1] and self.ys[0] <= y <= self.ys[1]

    def is_out(self, x, y):
        return y < self.ys[0]

    def max_h(self):
        return max(y for _, y in self.history)

    def tick(self):
        self.history.append((self.x, self.y))

        self.x += self.vx
        self.y += self.vy

        if self.vx > 0:
            self.vx -= 1
        elif self.vx < 0:
            self.vx += 1

        self.vy -= 1


def plot(p):
    xs, ys = p.xs, p.ys
    x_min, x_max = 0, max(max([x for x, _ in p.history]), xs[1])
    y_min, y_max = min(min([y for _, y in p.history]), ys[0]), max(
        [y for _, y in p.history]
    )
    print(f"x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")

    for y in range(y_max, y_min - 1, -1):
        for x in range(x_min, x_max + 1):
            if (x, y) in p.history:
                print("#", end="")
            elif p.is_in_range(x, y):
                print("T", end="")
            else:
                print(".", end="")
        print()


def run(p):
    done = False
    while not done:
        if success := p.is_in_range(p.x, p.y):
            done = True
        if p.is_out(p.x, p.y):
            done = True
        p.tick()

    return p.max_h(), success


def q1():
    xs, ys = get_input()
    max_h = 0
    for vx in range(0, xs[1] + 1):
        for vy in range(ys[0], -ys[0] + 1):
            p = Probe(vx, vy)
            h, success = run(p)
            if not success:
                continue
            max_h = max(h, max_h)
            # plot(p)
    return max_h


def q2():
    xs, ys = get_input()
    count = 0
    for vx in range(0, xs[1] + 1):
        for vy in range(ys[0], -ys[0] + 1):
            p = Probe(vx, vy)
            _, success = run(p)
            if not success:
                continue
            count += 1
            # plot(p)
    return count


def main():
    print(q1())
    print(q2())
    assert q1() == 8646
    assert q2() == 5945


if __name__ == "__main__":
    main()
