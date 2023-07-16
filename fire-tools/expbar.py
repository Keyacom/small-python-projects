#!/usr/bin/env python
from sys import argv, exit
from math import cbrt, floor


def usage():
    print("python expbar.py EXPERIENCE")


def exp_bar_length(n: int):
    level = floor(cbrt(n))
    if level != 1:
        prev_level_exp = level**3
    else:
        prev_level_exp = 0
    diff = (level + 1) ** 3 - prev_level_exp
    progress = n - prev_level_exp
    maxlen = 6
    newlen = progress * maxlen / diff
    return max(0.1, round(newlen, 1))


if __name__ == "__main__":
    if len(argv) != 2:
        print(f"error: wrong number of arguments (expected 1, got {len(argv) - 1})")
        usage()
        exit(2)
    try:
        exp = int(argv[1])
    except ValueError:
        print(f"error: invalid experience amount (expected a number, got {argv[1]!r})")
        exit(2)
    print("EXP bar length =", exp_bar_length(exp))
