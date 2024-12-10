from __future__ import annotations
import os
import argparse
import pytest

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    disk_map = ""
    for line in input_string.splitlines():
        disk_map += line.strip()

    blocks = _get_block(disk_map)
    reordered = _reorder(list(blocks))
    end = reordered.index(".")

    return sum([int(id) * i for i, id in enumerate(reordered[:end])])


def _get_block(disk_map: str) -> str:
    odd = len(disk_map) % 2 == 1

    if odd:
        disk_map, last = disk_map[0:-1], disk_map[-1]

    blocks = ""

    id = 0
    for i in range(0, len(disk_map), 2):
        file_length, free_space = disk_map[i], disk_map[i + 1]

        blocks += (str(id) * int(file_length)) + ("." * int(free_space))
        id += 1

    return blocks if not odd else blocks + (str(id) * int(last))


def _reorder(block: list[str]) -> str:
    left = 0
    right = len(block) - 1

    while block[left] != ".":
        left += 1

    while block[right] == ".":
        right -= 1

    while left < right:
        block[left], block[right] = block[right], block[left]

        left += 1
        while block[left] != ".":
            left += 1

        right -= 1
        while block[right] == ".":
            right -= 1

    return "".join(block)


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
2333133121414131402
"""
EXPECTED = 1928


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert solve(input_s) == expected


# MAIN ---------------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
