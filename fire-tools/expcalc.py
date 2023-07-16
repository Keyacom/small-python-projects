#!/usr/bin/env python
from getopt import getopt, GetoptError
from math import floor
from sys import argv, exit

FLAME_BURSTS_SHORT = "f:"
FLAME_BURSTS_LONG = ["flamebursts=", "flame-bursts=", "fbs="]
LEVEL_SHORT = "l:"
LEVEL_LONG = ["level=", "lv="]
HELP_SHORT = "h?"
HELP_LONG = ["help"]
CHALLENGE_SHORT = "c:"
CHALLENGE_LONG = ["challenge=", "chal="]
USAGE = """\
Usage:

python expcalc.py (-l LEVEL | --level=LEVEL) (-f FLAME_BURSTS | --flame-bursts=FLAME_BURSTS) (-c CHALLENGE | --challenge=CHALLENGE)
python expcalc.py (-h | --help)
"""


def calc_exp(fb: int, chal: int, level: int) -> int:
    return max(
        1,
        floor(
            (((fb * chal) / 5) * ((2 * chal + 10) / (chal + level + 10)) ** 2.5) / 3.5
        ),
    )


if __name__ == "__main__":
    try:
        options, args = getopt(
            argv[1:],
            FLAME_BURSTS_SHORT + LEVEL_SHORT + HELP_SHORT + CHALLENGE_SHORT,
            FLAME_BURSTS_LONG + LEVEL_LONG + HELP_LONG + CHALLENGE_LONG,
        )
    except GetoptError as exc:
        print(exc)
        print(USAGE)
        exit(2)
    if args:
        print("This command-line utility takes no rest arguments.")
        print(USAGE)
        exit(2)
    chal = None
    level = None
    fb = None
    for o, v in options:
        if o in ("-h", "--help", "-?"):
            print(USAGE)
            exit()
        if o in ("-f", "--flamebursts", "--flame-bursts", "-fb"):
            fb = int(v)
        elif o in ("-l", "--lv", "--level"):
            level = int(v)
        elif o in ("-c", "--chal", "--challenge"):
            chal = int(v)
        else:
            assert False, "unhandled option"

    if any(x is None for x in (chal, level, fb)):
        print("Incomplete arguments.")
        print(USAGE)
        exit(2)

    print("Challenge", chal)
    print("Level", level)
    print("Flame Bursts =", fb)
    print(
        "\nΔEXP =",
        calc_exp(fb, chal, level)  # type: ignore
        # Diagnostic ignores the fact I'm not allowing None past the if block!
    )
