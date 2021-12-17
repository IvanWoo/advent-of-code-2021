from __future__ import annotations

import fileinput
from typing import NamedTuple, Protocol
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[0]
INPUT_FILE = ROOT_DIR / "input.txt"

# fmt: off
class _Packet(Protocol):
    @property
    def version(self) -> int: ...
    @property
    def type_id(self) -> int: ...
    @property
    def n(self) -> int: ...
    @property
    def packets(self) -> tuple[_Packet, ...]: ...
# fmt: on


class Packet(NamedTuple):
    version: int
    type_id: int
    n: int = -1
    packets: tuple[_Packet, ...] = ()


def get_input():
    with fileinput.input(files=(INPUT_FILE)) as f:
        for line in f:
            return line.strip()


def h2b(hex_str):
    return "".join([bin(int(char, 16))[2:].zfill(4) for char in hex_str])


bin_str = h2b(get_input())


def parse(i):
    def _read(n):
        nonlocal i
        res = int(bin_str[i : i + n], 2)
        i += n
        return res

    version = _read(3)
    type_id = _read(3)

    if type_id == 4:
        # literal value
        n = 0
        chunk = _read(5)
        n += chunk & 0b1111
        while chunk & 0b10000:
            chunk = _read(5)
            n <<= 4
            n += chunk & 0b1111
        return i, Packet(version=version, type_id=type_id, n=n)
    else:
        mode = _read(1)
        if mode == 0:
            # 15 bits
            bits_len = _read(15)
            j = i
            i = i + bits_len
            packets = []
            while j < i:
                j, packet = parse(j)
                packets.append(packet)

            ret = Packet(
                version=version,
                type_id=type_id,
                packets=tuple(packets),
            )
            return i, ret
        else:
            # 11 bits
            sub_packets = _read(11)
            packets = []
            for _ in range(sub_packets):
                i, packet = parse(i)
                packets.append(packet)

            ret = Packet(
                version=version,
                type_id=type_id,
                packets=tuple(packets),
            )
            return i, ret


def val(packet: _Packet) -> int:
    if packet.type_id == 0:
        return sum(val(sub) for sub in packet.packets)
    elif packet.type_id == 1:
        ret = 1
        for sub in packet.packets:
            ret *= val(sub)
        return ret
    elif packet.type_id == 2:
        return min(val(sub) for sub in packet.packets)
    elif packet.type_id == 3:
        return max(val(sub) for sub in packet.packets)
    elif packet.type_id == 4:
        return packet.n
    elif packet.type_id == 5:
        return val(packet.packets[0]) > val(packet.packets[1])
    elif packet.type_id == 6:
        return val(packet.packets[0]) < val(packet.packets[1])
    elif packet.type_id == 7:
        return val(packet.packets[0]) == val(packet.packets[1])
    else:
        raise AssertionError(packet)


def q1():
    _, packet = parse(0)
    todo = [packet]
    total = 0
    while todo:
        item = todo.pop()
        total += item.version
        todo.extend(item.packets)
    return total


def q2():
    _, packet = parse(0)
    return val(packet)


def main():
    print(q1())
    print(q2())
    assert q1() == 934
    assert q2() == 912901337844


if __name__ == "__main__":
    main()
