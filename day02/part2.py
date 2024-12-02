from __future__ import annotations
import os
import argparse
import pytest

# CONSTANTS ----------------------------------------------------------------------------
DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT = os.path.join(DIR, "input.txt")


# BUSINESS LOGIC -----------------------------------------------------------------------
def solve(input_string: str) -> int:

    safe = 0

    for report in input_string.splitlines():
        levels = list(map(int, report.split()))

        # Variation of reports
        removed = [levels[0:i] + levels[i + 1 :] for i in range(len(levels))]

        for possibility in removed:
            mode: str | None = None
            for i in range(len(possibility) - 1):

                cur, nex = possibility[i], possibility[i + 1]

                # Reports are safe if they are monotonically decreasing or increasing.
                adj_mode = "d" if cur > nex else "i"
                mode = mode if mode != None else adj_mode
                if mode != adj_mode:
                    break

                # Reports that are safe also have have adjacent levels be at least one and
                # at most three apart.
                diff = abs(cur - nex)
                if not (diff > 0 and diff <= 3):
                    break

            else:
                safe += 1
                break

    return safe


# TEST CASES ---------------------------------------------------------------------------
INPUT_S = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
EXPECTED = 4


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
