# https://github.com/fogleman/AdventOfCode2021/blob/main/18.py
import ast
import fileinput
from pathlib import Path

import pytest


ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line


class Node:
    def __init__(
        self,
        x,
        depth=0,
    ):
        self.depth = depth
        if isinstance(x, list):
            self.L = Node(x[0], depth + 1)
            self.R = Node(x[1], depth + 1)
            self.leaf = False
        else:
            self.prev = self.next = None
            self.value = x
            self.leaf = True

    def visit(self):
        # preorder traversal using generator!
        yield self
        if not self.leaf:
            yield from self.L.visit()
            yield from self.R.visit()

    def __repr__(self):
        if self.leaf:
            return f"{self.value}"
        else:
            return f"[{self.L},{self.R}]"


def build(s: str) -> Node:
    root = Node(ast.literal_eval(s))
    # link the leafs beforehand
    # way much easier than walking the tree back and forth
    leafs = [x for x in root.visit() if x.leaf]
    for a, b in zip(leafs, leafs[1:]):
        a.next = b
        b.prev = a
    return root


def add(a, b):
    return build(f"[{a},{b}]")


def explode(node: Node):
    if node.L.prev:
        node.L.prev.value += node.L.value
    if node.R.next:
        node.R.next.value += node.R.value
    node.leaf = True
    node.value = 0


def split(node: Node):
    a = node.value // 2
    b = node.value - a
    n = Node([a, b], node.depth)
    node.leaf = False
    node.L = n.L
    node.R = n.R


def process(root):
    for node in root.visit():
        if node.depth >= 4 and not node.leaf:
            explode(node)
            return False
    for node in root.visit():
        if node.leaf and node.value >= 10:
            split(node)
            return False
    return True


def reduce(root):
    while True:
        root = build(repr(root))
        if process(root):
            return root


def magnitude(node: Node) -> int:
    if not node.leaf:
        return 3 * magnitude(node.L) + 2 * magnitude(node.R)
    return node.value


def q1():
    numbers = [build(x) for x in get_input()]

    node = numbers[0]
    for number in numbers[1:]:
        node = reduce(add(node, number))
    return magnitude(node)


def q2():
    numbers = [build(x) for x in get_input()]
    n = len(numbers)
    most = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            node = reduce(add(numbers[i], numbers[j]))
            most = max(most, magnitude(node))
    return most


def main():
    print(q1())
    print(q2())
    assert q1() == 3884
    assert q2() == 4595


@pytest.mark.parametrize(
    "input, expected",
    [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
    ],
)
def test_magnitude(input, expected):
    input = build(input)
    assert magnitude(input) == expected


if __name__ == "__main__":
    main()
