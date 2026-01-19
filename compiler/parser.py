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
# - Does our parse function eventually loop through and parse the whole input?
# - Should we be able to parse #\newline and equivalent escape sequances as characters?
#

from typing import Union

WSP = [' ', '\n', '\t', '\r']
ILLEGAL_CHARS = ['`']

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

    def parse(self):
        """
        Parses input strings of various objects.

        Returns:
            Atomic element or abstract syntax tree in the form of a Python list.

        Raises:
            EOFError: Unexpectedly reaches end of file.
            NotImplementedError: Non-integer value being parsed.
        """
        self.skip_whitespace()
        match self.peek():
            case '':
                raise EOFError("Unexpected end of input.")
            case c if c.isdigit():
                return self.parse_number()
            case '#':
                return self.parse_boolean_or_char()
            case '(':
                return self.parse_expression()
            case c:
                raise NotImplementedError(f"Found {c}.")

    def peek(self) ->str:
        """
        Get character at the front of input string.

        Returns:
            str: Character at front of input string.
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

    def parse_expression(self) -> list:
        """
        Parses expression from string.

        Returns:
            list: Atomic values of expression that have been parsed.

        Raises:
            TypeError: Invalid expression.
            NotImplementedError: Parse function for type not yet implemented.
        """
        # Consume opening parens.
        self.pos += 1

        match self.peek():
            case ')':
                return self.parse_empty_list()
            case c:
                raise NotImplementedError(f"Found {c}.")

    def parse_empty_list(self) -> list:
        """
        Parses empty list.

        Returns:
            list: Empty list.

        Raises:
            TypeError: Invalid empty list.
        """
        # Consume closing parens.
        self.pos += 1

        # If not whitespace or end of input, empty list is of invalid format.
        if not(self.peek() in WSP) and self.peek() != '':
            raise TypeError("Invalid list type.")

        return []

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

        # If not whitespace or end of input, number is of invalid format.
        if not(self.peek() in WSP) and self.peek() != '':
            raise TypeError("Invalid number type.")

        return num

    def parse_boolean_or_char(self) -> Union[str, bool]:
        """
        Parses boolean or character value from string.

        Returns:
            bool: Boolean value of string that has been parsed.
            str: Character value that was parsed.

        Raises:
            TypeError: Non-boolean or non-character found in string starting with #.
        """
        # Skip over '#'.
        self.pos += 1
        
        if self.peek() == 't' or self.peek() == 'T' or self.peek() == 'f' or self.peek() == 'F':
            return self.parse_boolean()
        elif self.peek() == '\\':
            return self.parse_char()
        else:
            raise TypeError("Invalid boolean or character type.")

    def parse_boolean(self) -> bool:
        """
        Parses boolean value from string.

        Returns:
            bool: Boolean value that has been parsed.

        Raises:
            TypeError: Non-boolean value found in string.
        """
        if self.peek() == 't' or self.peek() == 'T':
            ret_val = True
        elif self.peek() == 'f' or self.peek() == 'F':
            ret_val = False
        else:
            raise TypeError("Invalid boolean type.")
        
        self.pos += 1

        # If not whitespace or ind of input, number is of invalid format.
        if not(self.peek() in WSP) and self.peek() != '':
            raise TypeError("Invalid boolean type.")

        return ret_val

    def parse_char(self) -> str:
        """
        Parses character value from string.

        Returns:
            str: Character value that has been parsed.

        Raises:
            TypeError: Non-character value or illegal character value found in string.
        """
        # Skip over backslash.
        self.pos += 1

        if self.peek() in ILLEGAL_CHARS:
            raise TypeError("Illegal character.")
    
        ret_val = self.peek()
        
        self.pos += 1

        # If not whitespace or ind of input, number is of invalid format.
        if not(self.peek() in WSP) and self.peek() != '':
            raise TypeError("Invalid character type.")

        return ret_val

def scheme_parse(source: str) -> list:
    """
    Wrapper around parsing function for Scheme programs.

    Args:
        source (str): Scheme source program.

    Returns:
        list: Abstract syntax tree in the form of a Python list.
    """
    return Parser(source).parse()
