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

    area: list[list[str]] = []
    for line in input_string.splitlines():
        area.append(list(line))

    initial_pos: tuple[int, int] | None = None
    for x in range(len(area[0])):
        for y in range(len(area)):
            if area[y][x] == "^":
                initial_pos = (x, y)

    if not initial_pos:
        raise RuntimeError("Guard cannot be found!")

    visited = {initial_pos}
    direction_index: int = 0
    cur_pos = initial_pos

    # Loop while guard is in bounds
    while _in_bounds(cur_pos, area):
        visited.add(cur_pos)

        # Turn?
        if _turn(cur_pos, ORDER[direction_index], area):
            direction_index = (direction_index + 1) % len(ORDER)

        # Update position
        x, y = cur_pos
        x_delta, y_delta = ORDER[direction_index]
        cur_pos = (x + x_delta, y + y_delta)

    return len(visited)


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


def _turn(
    pos: tuple[int, int],
    direction: tuple[int, int],
    area: list[list[str]],
) -> bool:
    """Determines if guard needs to turn.
    The guard will need to move if there is a `#` in their way.

    Args:
        pos (tuple[int, int]): position of the guard
        direction (tuple[int, int]): direction the guard is going
        area (list[list[str]]): 2D array representing the area

    Returns:
        bool: returns True if the guard needs to turn, False otherwise
    """

    x, y = pos
    x_delta, y_delta = direction
    new_x, new_y = x + x_delta, y + y_delta
    return _in_bounds((new_x, new_y), area) and area[new_y][new_x] == "#"


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
