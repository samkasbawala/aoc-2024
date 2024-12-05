from __future__ import annotations
import os
import argparse
import pytest
import re

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
DIRECTIONS = [
    [-1, -1],  # up left
    [1, -1],  # up right
    [-1, 1],  # down left
    [1, 1],  # down right
]


def solve(input_string: str) -> int:

    grid: list[str] = []
    for line in input_string.splitlines():
        grid.append(line.strip())

    row, col = len(grid), len(grid[0])

    found = 0
    for y in range(row):
        for x in range(col):

            # Check for X-MAS
            if grid[y][x] == "A":
                found += check_x_mas(grid, x, y)

    return found


def check_x_mas(grid: list[str], x: int, y: int) -> int:

    # Won't be in bounds
    if not (1 <= x < len(grid[0]) - 1 and 1 <= y < len(grid) - 1):
        return 0

    # Forms X-MAS
    if (
        (grid[y - 1][x - 1] == "M" and grid[y + 1][x + 1] == "S")
        or (grid[y - 1][x - 1] == "S" and grid[y + 1][x + 1] == "M")
    ) and (
        (grid[y - 1][x + 1] == "M" and grid[y + 1][x - 1] == "S")
        or (grid[y - 1][x + 1] == "S" and grid[y + 1][x - 1] == "M")
    ):
        return 1

    return 0


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
EXPECTED = 9


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
