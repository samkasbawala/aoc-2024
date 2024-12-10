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
    reordered = _reorder(blocks)
    end = reordered.index(".")

    return sum([int(id) * i for i, id in enumerate(reordered[:end])])


def _get_block(disk_map: str) -> list[str]:
    """Converts disk_map to individual blocks

    Args:
        disk_map (str): disk block of data

    Returns:
        list[str]: returns a list where each item is a block
    """

    l: list[str] = []
    for i, val in enumerate(disk_map):
        if i % 2 == 0:
            l.extend([str(i // 2)] * int(val))
        else:
            l.extend(["."] * int(val))

    return l


def _reorder(block: list[str]) -> list[str]:
    """Reorders the block as to have contiguous blocks of memory filled

    Args:
        block (list[str]): _description_

    Returns:
        list[str]: Ordered blocks
    """

    left = 0
    right = len(block) - 1

    # Find first empty
    while block[left] != ".":
        left += 1

    # Find right most number
    while block[right] == ".":
        right -= 1

    while left < right:

        # swap
        block[left], block[right] = block[right], block[left]

        left += 1
        while block[left] != ".":
            left += 1

        right -= 1
        while block[right] == ".":
            right -= 1

    return block


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
