# Befunge [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple Befunge parser.

Befunge is an esoteric, stack-based programming language, designed to be two-dimensional.

## Befunge statement list

Each statement in Befunge is a single character.

|Character|Action
|-|-
|(ASCII digit)|Push that digit
|`+`|Pop `a` and `b`, push `a + b`
|`-`|Pop `a` and `b`, push `b - a`
|`*`|Pop `a` and `b`, push `a * b`
|`/`|Pop `a` and `b`, push `b // a`
|`%`|Pop `a` and `b`, push `int(b % a)`
|`` ` ``|Pop `a` and `b`, push `int(b > a)`
|`!`|Pop `x`, push `int(not x)`
|`<`|Move left
|`^`|Move up
|`>`|Move right
|`v`|Move down
|`?`|Move in a random cardinal direction
|`"`|String mode: Each new character pushes its code point, until the next `"`
|`:`|Duplicate the top value of the stack
|`\`|Swap two top values of the stack
|`$`|Discard the top value from the stack
|`\|`|Pop `x`, move up if `x != 0`, down otherwise
|`_`|Pop `x`, move left if `x != 0`, right otherwise
|`.`|Pop `x` and print it, followed by a space
|`,`|Pop `x` and print character at code point `x`
|`&`|Ask the user for a number and push it
|`~`|Ask the user for a character and push its code point
|`#`|Skip the next statement
|`p`|Pop `x`, `y`, and `v`, change character at position `(x, y)` to character at code point `v`
|`g`|Pop `x` and `y`, push code point of character at position `(x, y)`
|`@`|Exit
|(space)|Pass (null statement)

## CLI usage

### `python3 befunge.py INFILE [-o OUTFILE] [-W WIDTH] [-H HEIGHT]`

* `INFILE`: Specify the file name the Befunge code should be run from.
* `-o OUTFILE`: Specify the output file. If not specified, print everything to stdout.
  * Aliases: `--output`
* `-W WIDTH`: Specify the width of a Befunge program in characters. Defaults to 80.
  * Aliases: `--width`
* `-H HEIGHT`: Specify the height of a Befunge program in characters. Defaults to 25.
  * Aliases: `--height`

### `python3 befunge.py -h`

The `-h` option, which can be written as `--help` or `-?`, displays a help message
and exits.