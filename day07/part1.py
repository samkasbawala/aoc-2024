from __future__ import annotations
import os
import argparse
import pytest
import functools

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

    equations: list[tuple[int, tuple[int, ...]]] = []
    for line in input_string.splitlines():
        value, nums = line.split(":")
        nums_tup = tuple(map(int, nums.strip().split(" ")))
        equations.append((int(value.strip()), nums_tup))

    valid = list(filter(_can_make_valid, equations))
    return sum([eq[0] for eq in valid])


def _can_make_valid(equation: tuple[int, tuple[int, ...]]) -> bool:
    target, nums = equation[0], equation[1]
    return _can_make_valid_helper(target, nums[0], nums[1:])


@functools.cache
def _can_make_valid_helper(target: int, current: int, nums: tuple[int, ...]) -> bool:

    if target == current and len(nums) == 0:
        return True

    if current > target or len(nums) == 0:
        return False

    return _can_make_valid_helper(
        target,
        current * nums[0],
        nums[1:],
    ) or _can_make_valid_helper(
        target,
        current + nums[0],
        nums[1:],
    )


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
EXPECTED = 3749


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
