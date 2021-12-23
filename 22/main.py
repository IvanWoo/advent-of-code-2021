from __future__ import annotations
import fileinput
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from typing import List

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            yield line.strip()


@dataclass
class Op:
    state: int
    cuboid: Cuboid


def get_boundary(range_str):
    # x=10..12 => (10, 13)
    lo, hi = (int(n) for n in range_str.split("=")[1].split(".."))
    return (lo, hi + 1)


def parse() -> List[Op]:
    ops = []
    for line in get_input():
        state, ranges = line.split()
        xs, ys, zs = ranges.split(",")
        x0, x1 = get_boundary(xs)
        y0, y1 = get_boundary(ys)
        z0, z1 = get_boundary(zs)
        ops.append(Op(state == "on", Cuboid(x0, x1, y0, y1, z0, z1)))
    return ops


class Cuboid:
    def __init__(self, x0, x1, y0, y1, z0, z1) -> None:
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1

    @property
    def size(self) -> int:
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0)

    def intersects(self, other: Cuboid) -> bool:
        return (
            self.x0 <= other.x1 - 1
            and self.x1 - 1 >= other.x0
            and self.y0 <= other.y1 - 1
            and self.y1 - 1 >= other.y0
            and self.z0 <= other.z1 - 1
            and self.z1 - 1 >= other.z0
        )

    def contains(self, other: Cuboid) -> bool:
        return (
            self.x0 <= other.x0
            and self.x1 >= other.x1
            and self.y0 <= other.y0
            and self.y1 >= other.y1
            and self.z0 <= other.z0
            and self.z1 >= other.z1
        )

    def subtract(self, other: Cuboid) -> list[Cuboid]:
        if not self.intersects(other):
            return [self]
        elif other.contains(self):
            return []

        xs = sorted((self.x0, self.x1, other.x0, other.x1))
        ys = sorted((self.y0, self.y1, other.y0, other.y1))
        zs = sorted((self.z0, self.z1, other.z0, other.z1))

        res = []
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                for z0, z1 in zip(zs, zs[1:]):
                    cuboid = Cuboid(x0, x1, y0, y1, z0, z1)
                    if self.contains(cuboid) and not cuboid.intersects(other):
                        res.append(cuboid)
        return res


def q1():
    n = 50
    ops = parse()

    lights = dict()
    for op in ops:
        x0, x1 = op.cuboid.x0, op.cuboid.x1
        y0, y1 = op.cuboid.y0, op.cuboid.y1
        z0, z1 = op.cuboid.z0, op.cuboid.z1
        x0, x1 = max(x0, -n), min(x1, n)
        y0, y1 = max(y0, -n), min(y1, n)
        z0, z1 = max(z0, -n), min(z1, n)
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    lights[(x, y, z)] = op.state
    return sum(lights.values())


def q2():
    ops = parse()

    cuboids = []
    for op in ops:
        cuboids = [part for cub in cuboids for part in cub.subtract(op.cuboid)]
        if op.state:
            cuboids.append(op.cuboid)
    return sum(c.size for c in cuboids)


def main():
    print(q1())
    print(q2())
    assert q1() == 623748
    assert q2() == 1227345351869476


if __name__ == "__main__":
    main()
