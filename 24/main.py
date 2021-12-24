import fileinput
from pathlib import Path
from functools import lru_cache

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip().split()


ops = list(get_input())


@lru_cache(maxsize=None)
def search(op_idx, w_value, x_value, y_value, z_value):
    if z_value > 10 ** 6:
        return (False, "")

    if op_idx >= len(ops):
        return (z_value == 0, "")

    values = {"w": w_value, "x": x_value, "y": y_value, "z": z_value}

    def evaluate(var):
        return values[var] if var in values else int(var)

    op = ops[op_idx]
    if op[0] == "inp":
        # for d in range(9, 0, -1):
        for d in range(1, 10):
            values[op[1]] = d
            result = search(
                op_idx + 1, values["w"], values["x"], values["y"], values["z"]
            )

            if result[0]:
                print(result)
                return (True, str(d) + result[1])
        return (False, 0)

    second = evaluate(op[2])

    if op[0] == "add":
        values[op[1]] += second
    elif op[0] == "mul":
        values[op[1]] *= second
    elif op[0] == "div":
        if second == 0:
            return (False, 0)
        values[op[1]] //= second
    elif op[0] == "mod":
        if values[op[1]] < 0 or second <= 0:
            return (False, 0)
        values[op[1]] %= second
    elif op[0] == "eql":
        values[op[1]] = int(values[op[1]] == second)
    else:
        raise AssertionError
    return search(op_idx + 1, values["w"], values["x"], values["y"], values["z"])


def q1():
    return search(0, 0, 0, 0, 0)


def q2():
    return search(0, 0, 0, 0, 0)


def main():
    print(q1())
    # print(q2())
    # assert q1() == '98998519596997'
    # assert q2() == '31521119151421'


if __name__ == "__main__":
    main()
