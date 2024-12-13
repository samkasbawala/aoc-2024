from __future__ import annotations
import os
import argparse
import pytest
from collections import deque

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [
    UP,
    DOWN,
    LEFT,
    RIGHT,
]


def solve(input_string: str) -> int:

    area: list[str] = []
    for line in input_string.splitlines():
        area.append(line.strip())

    graph = _make_graph(area)
    return _get_cost(set(v for v in graph.values()))


def _make_graph(area: list[str]) -> dict[tuple[int, int], Node]:
    """Constructs a graph of plants based off the 2D representation of the garden.

    Args:
        area (list[list[str]]): 2D representation of the garden.

    Returns:
        dict[tuple[int, int], Node]: Dictionary, where each key is a coordinate and
        each value is a Node.
    """

    graph: dict[tuple[int, int], Node] = {}
    for y in range(len(area)):
        for x in range(len(area[y])):
            plant = area[y][x]
            graph[(x, y)] = graph.get((x, y), Node((x, y), plant))

            for dx, dy in DIRECTIONS:
                nx, ny = dx + x, dy + y

                if not (0 <= ny < len(area) and 0 <= nx < len(area[ny])):
                    continue

                new_plant = area[ny][nx]
                graph[(nx, ny)] = graph.get((nx, ny), Node((nx, ny), new_plant))

                # Neighbors
                if plant == new_plant:
                    graph[(nx, ny)].add_neighbor(graph[(x, y)])
                    graph[(x, y)].add_neighbor(graph[(nx, ny)])

    return graph


def _get_cost(nodes: set[Node]) -> int:
    """Gets cost of fencing for the area.
    Uses a modified BFS.

    Args:
        nodes (set[Node]): nodes representing the garden

    Returns:
        int: total cost
    """

    visited: set[Node] = set()
    cost = 0

    # Attempt to start a BFS at each node
    for node in nodes:

        # If already in a group, skip
        if node in visited:
            continue

        # Perform BFS as this start node, this will be one group
        d = deque([node])
        visited.add(node)

        fence = 4
        volume = 1

        while d:
            popped = d.pop()

            for neighbor in popped.get_neighbors():

                # Share a border
                if neighbor in visited:

                    # Need to consider a pair of adjacent plants only once
                    neighbor.remove_neighbor(popped)
                    fence -= 2

                    continue

                visited.add(neighbor)
                d.append(neighbor)

                fence += 4
                volume += 1

        cost += fence * volume

    return cost


class Node:
    def __init__(self, coordinates: tuple[int, int], plant: str):
        self._coordinates = coordinates
        self._plant = plant
        self._neighbors: set[Node] = set()

    def add_neighbor(self, other: Node) -> None:
        self._neighbors.add(other)

    def get_neighbors(self) -> set[Node]:
        return self._neighbors

    def remove_neighbor(self, other: Node):
        self._neighbors.discard(other)

    def __repr__(self):
        return f"Node(coordinates={self._coordinates}, plant={self._plant}, neighbors={[node._coordinates for node in self._neighbors]})"


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
EXPECTED = 1930


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
