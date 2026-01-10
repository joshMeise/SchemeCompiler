# parser.py - 
#
# Josh Meise
# 01-08-2026
# Description: 
#
# TODO: 
# -Implement bounds checking on integers.
# 
# Questions:
# - Does our parse function always return a list?
# - Does our parse function eventually loop through and parse the whole input?
#

WSP = [' ', '\n' '\t', '\r']

class Parser:
    """
    Class to handle parsing of Scheme program input text.

    Checks syntax of Scheme programs.
    Produces a list of tokens for use by compiler.

    Attributes:
        source (str): Scheme source program to be parsed.
        pos (int): Current position of parser in Scheme source program.
        length (int): Length of Scheme program.
    """

    def __init__(self, source: str):
        """
        Initializes the Parser object.

        Args:
            source (str): Scheme source code to be parsed.
        """
        self.source = source
        self.pos = 0
        self.length = len(source)

    def parse(self) -> list:
        """
        Parses input strings of various objects.

        Returns:
            list: Abstract syntax tree in the form of a Python list.

        Raises:
            EOFError: Unexpectedly reaches end of file.
            NotImplementedError: Non-integer value being parsed.
        """
        ast = []
        self.skip_whitespace()
        match self.peek():
            case '':
                raise EOFError("Unexpected end of input.")
            case c if c.isdigit():
                val = self.parse_number()
            case c:
                raise NotImplementedError(f"Parser only supports numbers currently. Found {c}.")

        ast.append(val)

        return ast

    def peek(self) -> char:
        """
        Get character at the front of input string.

        Returns:
            char: Character at front of input string.
        """
        # Return no character if end of input has been reached.
        if self.pos == self.length:
            return ''

        # Return front character in input string.
        c = self.source[self.pos]
        return c

    def skip_whitespace(self):
        """
        Removes leading whitespace in source code.
        """
        while self.peek() in WSP:
            self.pos += 1

    def parse_number(self) -> int:
        """
        Parses positive integer values from digit string.

        Returns:
            int: Integer value of string that has been parsed.

        Raises:
            TypeError: Non-digit found in integer string.
        """
        # Build ingeter from digit string.
        num = 0
        while self.peek().isdigit():
            num *= 10
            num += int(self.source[self.pos])
            self.pos += 1

        # If not whitespace, number is of invalid format.
        if not(self.peek() in WSP) and self.peek() != '':
            raise TypeError("Invalid number type.")

        return num

def scheme_parse(source: str) -> list:
    """
    Wrapper around parsing function for Scheme programs.

    Args:
        source (str): Scheme source program.

    Returns:
        list: Abstract syntax tree in the form of a Python list.
    """
    return Parser(source).parse()
