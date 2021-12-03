import fileinput
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line


def q1():
    def parse(cmd):
        keyword, _unit = cmd.split()
        unit = int(_unit)
        if keyword == "forward":
            return (unit, 0)
        elif keyword == "up":
            return (0, -unit)
        elif keyword == "down":
            return (0, unit)

    def run(cmd, ans):
        x, y = ans
        dx, dy = parse(cmd)
        return (x + dx, y + dy)

    # (horizontal, depth)
    ans = (0, 0)
    for cmd in get_input():
        ans = run(cmd, ans)
    return ans[0] * ans[1]


def q2():
    def parse(cmd):
        keyword, _unit = cmd.split()
        unit = int(_unit)
        if keyword == "forward":
            return (unit, unit, 0)
        elif keyword == "up":
            return (0, 0, -unit)
        elif keyword == "down":
            return (0, 0, unit)

    def run(cmd, ans):
        x, y, z = ans
        dx, dy, dz = parse(cmd)
        return (x + dx, y + dy * z, z + dz)

    # (horizontal, depth, aim)
    ans = (0, 0, 0)
    for cmd in get_input():
        ans = run(cmd, ans)
    return ans[0] * ans[1]


def main():
    print(q1())
    print(q2())
    assert q1() == 2027977
    assert q2() == 1903644897


if __name__ == "__main__":
    main()
