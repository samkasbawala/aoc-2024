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

    area: list[list[int]] = []
    for line in input_string.splitlines():
        area.append(list(map(int, line.strip())))

    graph = _create_graph(area)
    starting_nodes = [v for v in graph.values() if v.get_height() == 0]

    return sum([_bfs(node, 9) for node in starting_nodes])


def _create_graph(area: list[list[int]]) -> dict[tuple[int, int], Node]:
    """Creates a graph using the 2D representation of the area

    Args:
        area (list[list[int]]): 2D array representation of the area

    Returns:
        dict[tuple[int, int], Node]: Key is the coordinate, Value is the Node
    """

    graph: dict[tuple[int, int], Node] = dict()
    for y in range(len(area)):
        for x in range(len(area[y])):

            # Create node if it doesn't exist
            graph[(x, y)] = graph.get((x, y), Node(x, y, area[y][x]))
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy

                # Out of bounds
                if not (0 <= ny < len(area) and 0 <= nx < len(area[ny])):
                    continue

                # Create neighbor node if doesn't exist
                graph[(nx, ny)] = graph.get((nx, ny), Node(nx, ny, area[ny][nx]))

                # Add neighbor if traversable
                if graph[(x, y)].get_height() + 1 == graph[(nx, ny)].get_height():
                    graph[(x, y)].add_neighbor(graph[((nx, ny))])

    return graph


def _bfs(starting_node: Node, target_height: int) -> int:
    """Conducts a BFS search from the starting node to see if it can reach a node with
    the desired target height.

    Args:
        starting_node (Node): starting node
        target_height (int): desired height of a node we want to be able to reach

    Returns:
        int: number of times we hit a unique node with height target_height
    """
    print(starting_node)

    q: deque[Node] = deque()
    visited: set[Node] = set()

    visited.add(starting_node)
    q.append(starting_node)

    reachable = 0
    while q:
        node = q.popleft()

        for neighbor in node.get_neighbors():
            if neighbor in visited:
                continue

            if neighbor.get_height() == target_height:
                reachable += 1

            visited.add(neighbor)
            q.append(neighbor)

    return reachable


class Node:
    def __init__(self, x: int, y: int, h: int):
        self.__id = (x, y)
        self.__height = h
        self.__neighbors: set[Node] = set()

    def add_neighbor(self, other: Node) -> None:
        self.__neighbors.add(other)

    def get_height(self) -> int:
        return self.__height

    def get_neighbors(self) -> set[Node]:
        return self.__neighbors

    def __repr__(self) -> str:
        return f"Node(loc={self.__id}, h={self.__height}): neighbors={[n.__id for n in self.__neighbors]}"


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
EXPECTED = 36


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
