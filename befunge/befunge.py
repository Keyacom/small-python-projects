import sys


class Befunge:
    """
    ``Befunge`` objects contain the code and size of executed Befunge code,
    and it can be executed from such objects.
    """

    class Error(ValueError):
        pass

    def __init__(self, code: str, /, width: int = 80, height: int = 25) -> None:
        self.pos = [0, 0]
        self.stack = []
        self.width = width
        self.height = height
        self.code = code  # Intentionally placed after width and height setting

        # Various parsing variables
        self.dir = ">"
        self.in_string = False
        self.skipping = False

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, value) -> None:
        """
        This function exists as a DRY-friendly solution for setting the ``code``
        attribute of ``Befunge`` objects to immediately change the nested
        ``code_to_exec`` list.
        """
        self._code = value
        self.code_to_exec = []
        for line in value.splitlines():
            # list(...) to make it mutable
            self.code_to_exec.append(list(f"{line:<{self.width}}"))

        _length = len(self.code_to_exec)
        for _ in range(self.height - _length):
            self.code_to_exec.append([" "] * self.width)

    def exec_chr(
        self, char: str, /, errors: str | None = "strict", file=sys.stdout
    ) -> None:
        if self.in_string:
            if char == '"':
                self.in_string = False
            else:
                self.stack.append(ord(char))
        else:
            match char:
                case "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    self.stack.append(int(char))
                case "+" | "-" | "*" | "/" | "%" | "`":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    ops = {
                        "+": "__add__",
                        "-": "__sub__",
                        "*": "__mul__",
                        "/": "__floordiv__",
                        "%": "__mod__",
                        "`": "__gt__"
                    }
                    self.stack.append(int(getattr(b, ops[char])(a)))
                case "!":
                    c = self.stack.pop()
                    self.stack.append(int(not c))
                case "_" | "|":
                    x = self.stack.pop()
                    dirs = {"_": {True: "<", False: ">"}, "|": {True: "^", False: "v"}}
                    self.dir = dirs[char][x != 0]
                case "#":
                    self.skipping = True
                case ":":
                    _ = 0
                    if len(self.stack) != 0:
                        _ = self.stack[-1]
                    else:
                        self.stack.append(0)
                    self.stack.append(_)
                case "$":
                    self.stack.pop()  # Discard the top value from the stack
                case "\\":
                    _ = [0, 0] + self.stack[-3:-1]
                    self.stack[-3:-1] = _[-3:-1][::-1]
                case ".":
                    print(self.stack.pop(), end=" ", file=file)
                case ",":
                    print(chr(self.stack.pop()), end="", file=file)
                case "&":
                    self.stack.append(int(input()))
                case "~":
                    self.stack.append(ord(input()[0]))
                case "?":
                    from random import randint

                    # import can be here, it's the only place where it's used
                    self.dir = "^<v>"[randint(0, 3)]
                case "g":
                    x, y = 0, 0
                    try:
                        x, y = self.stack[-3:-1][::-1]
                    except ValueError:
                        pass
                    self.stack.append(ord(self.code_to_exec[y][x]))
                case "p":
                    x, y, v = 0, 0, " "
                    try:
                        x, y, v = self.stack[-4:-1][::-1]
                    except ValueError:
                        pass
                    self.code_to_exec[y][x] = v
                case '"':
                    self.in_string = True
                case "<" | "^" | ">" | "v":
                    self.dir = char
                case "@" | " ":
                    pass
                    # This section is left empty intentionally for these reasons:
                    #
                    # @: its behavior is controlled by the main loop
                    # (space): means nothing
                case _:
                    if errors == "strict" or errors is None:
                        from textwrap import wrap

                        cc = hex(ord(char))[2:]
                        cc = cc.rjust(max([4, len(cc) // 4 * 4]), "0")
                        raise Befunge.Error(
                            "\n".join(
                                wrap(
                                    "\x1b[37;41mSyntax error\x1b[0m: "
                                    f'Illegal char U+{cc} "{repr(char)[1:-1]}" '
                                    f"at {tuple(self.pos)}. Perhaps you forgot to"
                                    " activate string mode or set `errors` to "
                                    "something other than `'strict'`?",
                                    80,
                                )
                            )
                        )

    def main_loop(self, file=sys.stdout):
        ch = self.code_to_exec[0][0]
        while 1:
            if not self.skipping:
                self.exec_chr(ch, file=file)
            else:
                self.skipping = False
            match self.dir:
                case "^":
                    self.pos[1] -= 1
                case "<":
                    self.pos[0] -= 1
                case ">":
                    self.pos[0] += 1
                case "v":
                    self.pos[1] += 1

            if self.pos[0] not in range(self.width):
                self.pos[0] -= self.width

            if self.pos[1] not in range(self.height):
                self.pos[1] -= self.height

            ch = self.code_to_exec[self.pos[1]][self.pos[0]]
            if not self.in_string and ch == "@":
                break


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser(
        description="""\
Parse Befunge code. Currently, reading code is supported only from files.""",
        add_help=False,
    )
    arg_parser.add_argument(
        "input",
        type=argparse.FileType("r", encoding="utf8"),
        help="\x1b[7mInput file\x1b[0m",
    )
    arg_parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w", encoding="utf8"),
        help="\x1b[7mOutput file\x1b[0m: if not provided, defaults to sys.stdout.",
        default=sys.stdout,
    )
    arg_parser.add_argument(
        "-W",
        "--width",
        type=int,
        default=80,
        help="\x1b[7mWidth\x1b[0m: Provides a custom width for a Befunge program. \
If not provided, defaults to 80.",
    )
    arg_parser.add_argument(
        "-H",
        "--height",
        type=int,
        default=25,
        help="\x1b[7mHeight\x1b[0m: Provides a custom height for a Befunge \
program. If not provided, defaults to 25.",
    )
    arg_parser.add_argument(
        "-h",
        "--help",
        "-?",
        action="help",
        help="\x1b[7mHelp\x1b[0m: Display this message and exit.",
    )
    args = arg_parser.parse_args()

    befunge = Befunge(args.input.read(), width=args.width, height=args.height)
    befunge.main_loop(file=args.output)
