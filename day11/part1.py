from __future__ import annotations
import os
import argparse
import pytest
from functools import cache

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str, input_blinks: int) -> int:

    stones: list[str] = []
    for line in input_string.splitlines():
        stones.extend(line.strip().split(" "))

    # Count stones
    stones_count: dict[str, int] = dict()
    for stone in stones:
        stones_count[stone] = stones_count.get(stone, 0) + 1

    # Process stones for each blink
    for _ in range(input_blinks):
        stones_count = _blink(stones_count)

    return sum(v for v in stones_count.values())


def _blink(stones_count: dict[str, int]) -> dict[str, int]:
    """Return a count of each stone after a blink

    Args:
        stones_count (dict[str, int]): Dictionary where key is the stone and the value
        is the number of times a stone appears.

    Returns:
        dict[str, int]: An updated dictionary of the stone counts
    """

    result: dict[str, int] = dict()
    for stone, count in stones_count.items():
        stones = process(stone)
        for p_stone in stones:
            result[p_stone] = result.get(p_stone, 0) + count

    return result


# Cache because i'm too lazy to implement memoization LOL
@cache
def process(stone: str) -> list[str]:
    """Process the stone. Rules follow the following order:
    1. If the stone is engraved with the number 0, it is replaced by a stone engrave
    with the number 1.

    2. If the stone is engraved with a number that has an even number of digits, it is
    replaced by two stones. The left half of the digits are engraved on the new left
    stone, and the right half of the digits are engraved on the new right stone. (The
    new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)

    3. If none of the other rules apply, the stone is replaced by a new stone; the old
    stone's number multiplied by 2024 is engraved on the new stone.

    Args:
        stone (str): stone's number as a string

    Returns:
        list[str]: returns the list of resulting stones after processing it
    """

    # Rule 1
    if int(stone) == 0:
        return ["1"]

    # Rule 2
    n = len(stone)
    if n % 2 == 0:
        return [stone[: n // 2], str(int(stone[n // 2 :]))]

    # Rule 3
    return [str(int(stone) * 2024)]


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
125 17
"""
INPUT_BLINKS = 25
EXPECTED = 55312


@pytest.mark.parametrize(
    ("input_s", "input_blinks", "expected"),
    ((INPUT_S, INPUT_BLINKS, EXPECTED),),
)
def test(input_s: str, input_blinks: int, expected: int) -> None:
    assert solve(input_s, input_blinks) == expected


# MAIN ---------------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read(), 25))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
