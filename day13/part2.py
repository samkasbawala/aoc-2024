from __future__ import annotations
import os
import argparse
import pytest
import re
import numpy as np

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    machines: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
    for line in input_string.strip().split("\n\n"):
        a, b, prize = line.split("\n")

        movement_pattern = r"\+(\d+)"
        xa, ya = re.findall(movement_pattern, a)
        xb, yb = re.findall(movement_pattern, b)

        prize_pattern = r"=(\d+)"
        px, py = re.findall(prize_pattern, prize)
        machines.append(
            (
                (int(xa), int(ya)),
                (int(xb), int(yb)),
                (int(px) + 10000000000000, int(py) + 10000000000000),
            )
        )

    return sum([_process_machine(a, b, prize) for a, b, prize in machines])


def _process_machine(
    a: tuple[int, int],
    b: tuple[int, int],
    prize: tuple[int, int],
) -> int:

    ax, ay = a
    bx, by = b
    px, py = prize

    # Linear combinations: https://python-course.eu/numerical-programming/linear-combinations-in-python.php
    x = np.array(
        [
            [ax, bx],
            [ay, by],
        ]
    )
    y = np.array([px, py])
    sa, sb = np.rint(np.linalg.solve(x, y))

    if sa * ax + sb * bx == px and sa * ay + sb * by == py:
        return int(3 * sa + sb)

    return 0


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
EXPECTED = 875318608908


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
