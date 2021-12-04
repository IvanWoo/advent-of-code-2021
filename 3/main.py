import fileinput
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


def bin_to_dec(bin_str):
    return int(bin_str, 2)


def q1():
    input_data = list(get_input())

    gamma = ""
    epsilon = ""
    counters = defaultdict(lambda: defaultdict(int))
    for line in input_data:
        for index, char in enumerate(line):
            counters[index][char] += 1

    for _, v in counters.items():
        if v["1"] >= v["0"]:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    return bin_to_dec(gamma) * bin_to_dec(epsilon)


def q2():
    def count(input_data, included, pos):
        counter = defaultdict(int)
        for is_included, line in zip(included, input_data):
            if not is_included:
                continue
            counter[line[pos]] += 1
        return counter

    def helper(input_data, target):
        rates = {"gamma": "", "epsilon": ""}
        included = [True] * len(input_data)
        n = len(input_data[0])
        product = None
        for pos in range(n + 1):
            if sum(included) == 1:
                product = input_data[included.index(True)]
                break
            counters = count(input_data, included, pos)
            if counters["1"] >= counters["0"]:
                rates["gamma"] += "1"
                rates["epsilon"] += "0"
            else:
                rates["gamma"] += "0"
                rates["epsilon"] += "1"
            included = [line.startswith(rates[target]) for line in input_data]
        return bin_to_dec(product)

    input_data = list(get_input())
    return helper(input_data, "gamma") * helper(input_data, "epsilon")


def main():
    print(q1())
    print(q2())
    assert q1() == 3847100
    assert q2() == 4105235


if __name__ == "__main__":
    main()
