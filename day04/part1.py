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
    (-1, 0),  # left
    (1, 0),  # right
    (0, 1),  # down
    (0, -1),  # up
    (-1, -1),  # up left
    (1, -1),  # up right
    (-1, 1),  # down left
    (1, 1),  # down right
]


def solve(input_string: str) -> int:

    grid: list[str] = []
    for line in input_string.splitlines():
        grid.append(line.strip())

    row, col = len(grid), len(grid[0])

    found = 0
    for y in range(row):
        for x in range(col):
            for direction in DIRECTIONS:
                found += look_for_word_at(grid, x, y, "XMAS", direction)

    return found


def look_for_word_at(
    grid: list[str], x: int, y: int, word: str, direction: tuple[int, int]
) -> int:

    # word found
    if len(word) == 0:
        return 1

    # out of bounds?
    if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[y]):
        return 0

    if word[0] != grid[y][x]:
        return 0

    x_delta, y_delta = direction
    return look_for_word_at(grid, x + x_delta, y + y_delta, word[1:], direction)


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
EXPECTED = 18


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
