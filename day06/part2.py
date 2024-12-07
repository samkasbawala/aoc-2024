from __future__ import annotations
import os
import argparse
import pytest

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
ORDER: list[tuple[int, int]] = [UP, RIGHT, DOWN, LEFT]


def solve(input_string: str) -> int:

    # Area
    area: list[list[str]] = []
    for line in input_string.splitlines():
        area.append(list(line))

    # Initial guard position
    initial_pos: tuple[int, int] | None = None
    for x in range(len(area[0])):
        for y in range(len(area)):
            if area[y][x] == "^":
                initial_pos = (x, y)
    if not initial_pos:
        raise RuntimeError("Guard cannot be found!")

    direction_index = 0
    cur_pos = initial_pos
    visited = {(*cur_pos, direction_index)}

    while True:
        x, y, direction_index = _move(cur_pos, direction_index, area)

        # Out of bounds
        if x is None or y is None:
            break

        visited.add((x, y, direction_index))
        cur_pos = (x, y)

    return len(visited)


def _move(
    pos: tuple[int, int],
    direction_index: int,
    area: list[list[str]],
) -> tuple[int, int, int]:

    x, y = pos
    while True:
        x_delta, y_delta = ORDER[direction_index]
        new_x, new_y = x + x_delta, y + y_delta

        if not _in_bounds((new_x, new_y), area):
            return None, None, None

        # Moveable
        if area[new_y][new_x] != "#":
            return (new_x, new_y, direction_index)

        # Needs to turn
        else:
            direction_index = (direction_index + 1) % len(ORDER)


def _in_bounds(
    pos: tuple[int, int],
    area: list[list[str]],
) -> bool:
    """Determines whether or not the the current position is within the area of the grid

    Args:
        pos (tuple[int, int]): position of the guard
        area (list[list[str]]): 2D array representing the area

    Returns:
        bool: returns True if position is in bounds, False otherwise
    """
    x, y = pos
    return 0 <= x < len(area[0]) and 0 <= y < len(area)


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
EXPECTED = 41


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
