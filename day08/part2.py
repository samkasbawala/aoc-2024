from __future__ import annotations
import os
import argparse
import pytest

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    area: list[list[str]] = []
    for line in input_string.splitlines():
        trimmed = line.strip()
        area.append(list(trimmed))

    # Find coordinates for each signal
    coordinates = _find_coordinates(area)

    # Find anti nodes
    anti_nodes_coordinates = _find_anti_nodes(coordinates, area)

    return len(anti_nodes_coordinates)


def _find_coordinates(
    area: list[list[str]],
) -> dict[str, set[tuple[int, int]]]:
    """Finds the coordinates for each signal.

    Args:
        area (list[list[str]]): 2D array representing the array

    Returns:
        dict[str, set[tuple[int, int]]]: A map where each key is the signal and the
            value is the set of tuples of points where the signals are.
    """

    coordinates: dict[str, set[tuple[int, int]]] = dict()
    for y in range(len(area)):
        for x in range(len(area[y])):
            if area[y][x] == ".":
                continue
            coordinates[area[y][x]] = coordinates.get(area[y][x], set())
            coordinates[area[y][x]].add((x, y))

    return coordinates


def _find_anti_nodes(
    coordinates: dict[str, set[tuple[int, int]]],
    area: list[list[str]],
) -> set[tuple[int, int]]:
    """Finds anti nodes for all signals

    Args:
        coordinates (dict[str, set[tuple[int, int]]]): A map where each key is the signal
            and the value are the coordinates

    Returns:
        set[tuple[int, int]]: set of coordinates of anti nodes
    """

    anti_nodes: set[tuple[int, int]] = set()
    for _, locations in coordinates.items():
        anti_nodes = anti_nodes.union(_process_signal(locations, area))

    return anti_nodes


def _process_signal(
    locations: set[tuple[int, int]],
    area: list[list[str]],
) -> set[tuple[int, int]]:
    """Business logic for finding anti nodes given one list of coordinates

    Args:
        locations (set[tuple[int, int]]): coordinates of signal

    Returns:
        set[tuple[int, int]]: a set of coordinates of anti  nodes
    """

    # p1 will always be to the left of p2
    locations_list = sorted(list(locations), key=lambda x: x[0])
    anti_nodes = set()
    for i in range(len(locations) - 1):
        for j in range(i + 1, len(locations)):
            p1, p2 = locations_list[i], locations_list[j]

            # All antennas are anti nodes
            anti_nodes.add(p1)
            anti_nodes.add(p2)

            (rise, run) = _find_slope(p1, p2)
            x1, y1 = p1
            x2, y2 = p2

            # Add points in line
            cur_pos = (x1 - run, y1 - rise)
            while _in_bounds(cur_pos, area):
                anti_nodes.add(cur_pos)
                x, y = cur_pos
                cur_pos = (x - run, y - rise)

            cur_pos = (x2 + run, y2 + rise)
            while _in_bounds(cur_pos, area):
                anti_nodes.add(cur_pos)
                x, y = cur_pos
                cur_pos = (x + run, y + rise)

    return anti_nodes


def _find_slope(
    p1: tuple[int, int],
    p2: tuple[int, int],
) -> tuple[int, int]:
    """Returns a tuple (rise, run) indicating the slope between the two points

    Args:
        p1 (tuple[int, int]): point 1
        p2 (tuple[int, int]): point 2

    Returns:
        tuple[int, int]: (rise, run)
    """
    x1, y1 = p1
    x2, y2 = p2

    return (y2 - y1, x2 - x1)


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
    return 0 <= y < len(area) and 0 <= x < len(area[y])


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
EXPECTED = 34


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
