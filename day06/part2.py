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

    prospects = _get_visited(initial_pos, area, 0)
    prospects.remove(initial_pos)

    return len(list(filter(lambda x: _loop(initial_pos, x, area, 0), prospects)))


def _loop(
    initial_pos: tuple[int, int],
    obstacle: tuple[int, int],
    area: list[list[str]],
    direction_index: int,
) -> bool:
    """Returns a boolean indicating whether adding an obstacle at position `obstacle`
    will result in an infinite loop.

    Args:
        initial_pos (tuple[int, int]): initial position
        obstacle (tuple[int, int]): coordinate of obstacle
        area (list[list[str]]): 2D array representing area
        direction_index (int): direction the guard is traveling

    Returns:
        bool: Returns True if set up will result in an infinite loop, otherwise False
    """

    obs_x, obs_y = obstacle
    area[obs_y][obs_x] = "#"

    cur_pos = initial_pos
    visited = set()

    # Loop until we come back to a spot facing in the same direction
    while (*cur_pos, direction_index) not in visited:
        visited.add((*cur_pos, direction_index))

        # Break out if we have left the area
        if not _in_bounds(cur_pos, area):
            break

        # Turn?
        while _turn(cur_pos, ORDER[direction_index], area):
            direction_index = (direction_index + 1) % len(ORDER)

        # Update position
        x, y = cur_pos
        x_delta, y_delta = ORDER[direction_index]
        cur_pos = (x + x_delta, y + y_delta)

    # Reach this branch if we have exited out of the loop naturally
    else:
        area[obs_y][obs_x] = "."
        return True

    area[obs_y][obs_x] = "."
    return False


def _get_visited(
    initial_pos: tuple[int, int],
    area: list[list[str]],
    direction_index: int,
) -> set[tuple[int, int]]:
    """Return visited coordinates with the passed in conditions.

    Args:
        initial_pos (tuple[int, int]): initial position of guard
        area (list[list[str]]): 2D array representing area
        direction_index (int): direction the guard is traveling

    Returns:
        set[tuple[int, int]]: distinct locations visited by the guard
    """

    visited = set()
    cur_pos = initial_pos

    # Loop while guard is in bounds
    while _in_bounds(cur_pos, area):
        visited.add(cur_pos)

        # Turn?
        while _turn(cur_pos, ORDER[direction_index], area):
            direction_index = (direction_index + 1) % len(ORDER)

        # Update position
        x, y = cur_pos
        x_delta, y_delta = ORDER[direction_index]
        cur_pos = (x + x_delta, y + y_delta)

    return visited


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
EXPECTED = 6


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
