from __future__ import annotations
import os
import argparse
import pytest

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    raw_lines = input_string.splitlines()
    index = raw_lines.index("")  # Index of rules splitting
    rules, updates = raw_lines[:index], raw_lines[index + 1 :]

    # Build graph of rules
    graph: dict[int, Rule] = {}
    for rule in rules:
        pre, dep = list(map(int, rule.split("|")))

        graph[pre] = graph.get(pre, Rule(pre))
        graph[dep] = graph.get(dep, Rule(dep))

        graph[pre].add_dependent(graph[dep])
        graph[dep].add_prerequisite(graph[pre])

    updates_clean = [list(map(int, update.split(","))) for update in updates]
    invalid_updates = list(
        filter(lambda update: not is_valid_update(update, graph), updates_clean)
    )
    invalid_updates_fixed = list(
        map(lambda update: order_invalid_update(update, graph), invalid_updates)
    )

    return sum(update[len(update) // 2] for update in invalid_updates_fixed)


class Rule:
    def __init__(self, id: int):
        self.id = id
        self._dependents: set[Rule] = set()
        self._prerequisites: set[Rule] = set()

    def add_dependent(self, other: Rule) -> None:
        self._dependents.add(other)

    def add_prerequisite(self, other: Rule) -> None:
        self._prerequisites.add(other)

    def is_prerequisite(self, other: Rule) -> bool:
        """Returns a boolean indicating if self is a prerequisite of other.

        Args:
            other (Rule): other Rule to be checked with

        Returns:
            bool: if self is a prerequisite of other
        """
        return other in self._dependents and other not in self._prerequisites


def is_valid_update(update: list[int], graph: dict[int, Rule]) -> bool:
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update), 1):
            pre, dep = graph[update[i]], graph[update[j]]
            if not pre.is_prerequisite(dep):
                return False

    return True


def order_invalid_update(update: list[int], graph: dict[int, Rule]) -> list[int]:
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update), 1):
            pre, dep = graph[update[i]], graph[update[j]]
            if not pre.is_prerequisite(dep):
                update[i], update[j] = update[j], update[i]

    return update


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
EXPECTED = 123


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
