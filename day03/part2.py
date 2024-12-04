from __future__ import annotations
import os
import argparse
import pytest
import re

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    s = ""
    for line in input_string.splitlines():
        s += line

    # First find the don't operations
    donts = s.split("don't")

    # Get each of the do operations within each don't
    dos = [donts[0]]
    do_pattern = r"do\(\)(.*)"
    for dont in donts[1:]:
        dos.extend(re.findall(do_pattern, dont))

    # Find all the operations
    mul_pattern = r"mul\((\d+),(\d+)\)"
    pairs = []
    for do in dos:
        pairs.extend(re.findall(mul_pattern, do))

    # For each operation, multiply
    product = 0
    for x, y in pairs:
        product += int(x) * int(y)

    return product


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
EXPECTED = 48


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
