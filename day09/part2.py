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

    return sum([int(id) * i for i, id in enumerate(reordered) if id != "."])


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
    """Reorders the block as to move right most files to the left as whole file.

    Args:
        block (list[str]): list of individual blocks

    Returns:
        list[str]: Ordered blocks
    """

    files = sorted(map(int, set(filter(lambda x: x != ".", block))))

    for file in reversed(files):
        block = _move(block, str(file))

    return block


def _move(block: list[str], file: str) -> list[str]:
    """Moves the file in the block.

    Args:
        block (list[str]): list of individual blocks
        file (str): file to move

    Returns:
        list[str]: new block after file has been moved
    """

    l_i = _find_start(block, file)

    if l_i == -1:
        return block

    r_i = block.index(file)
    end = block.count(file)
    block[l_i : end + l_i], block[r_i : end + r_i] = (
        block[r_i : end + r_i],
        block[l_i : end + l_i],
    )

    return block


def _find_start(block: list[str], file: str) -> int:
    """Finds the start index of empty memory that can fit the file.
    Returns -1 if there is no place in the memory to fit the whole file.

    Args:
        block (list[str]): list of individual blocks
        file (str): file that needs to be moved

    Returns:
        int: index of starting position of where the file will need to move to.
    """
    right = block.index(file)
    count = block.count(file)

    num = 0
    for i, val in enumerate(block[:right]):
        if val == ".":
            num += 1

            if count == num:
                return i - num + 1

        else:
            num = 0

    return -1


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
2333133121414131402
"""
EXPECTED = 2858


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
