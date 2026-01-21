# parser.py - 
#
# Josh Meise
# 01-08-2026
# Description: 
#
# Currently haev it that we can only accept one expression per line.
# - Consumes whitespace at end and makes sure we haev reached end of input.
#
# TODO: 
# -Implement bounds checking on integers.
# - 
# 
# Questions:
# - Does our parse function eventually loop through and parse the whole input?
# - Should we be able to parse #\newline and equivalent escape sequances as characters?
# - Should return types of each expression be checked in the parser so that doing something line (add1 (integer->char 3)) is illegal?
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
                val = self.parse_number()
            case '#':
                val = self.parse_boolean_or_char()
            case '(':
                val = self.parse_expression()
            case c:
                raise NotImplementedError(f"Found {c}.")

        # Ensure that whitespace follows.
        self.skip_whitespace()
        
        # If not whitespace or end of input, empty list is of invalid format.
        if self.peek() != '':
            raise TypeError("Invalid type.")

        return val

    def parse_expression(self) -> list:
        """
        Parses expression from string.

        Returns:
            list: AST containing expressiont aht have been parsed.

        Raises:
            TypeError: Invalid expression.
            NotImplementedError: Parse function for type not yet implemented.
        """
        # Consume opening parens.
        self.pos += 1

        # Skip whitespace.
        self.skip_whitespace()

        ast = []

        match self.peek():
            case ')':
                return self.parse_empty_list()
            # Contains another expression.
            case '(':
                ast.append(self.parse_expression())
            case _:
                match self.peek_word():
                    case "add1":
                        return self.parse_unary_int_arg("add1")
                    case "sub1":
                        return self.parse_unary_int_arg("sub1")
                    case "integer->char":
                        return self.parse_unary_int_arg("integer->char")
                    case "char->integer":
                        return self.parse_unary_char_arg("char->integer")
                    case "null?":
                        return self.parse_unary_any_arg("null?")
                    case "zero?":
                        return self.parse_unary_int_arg("zero?")
                    case "not":
                        return self.parse_unary_any_arg("not")
                    case "integer?":
                        return self.parse_unary_any_arg("integer?")
                    case "boolean?":
                        return self.parse_unary_any_arg("boolean?")
                    case "+":
                        return self.parse_binary_int_args("+")
                    case "*":
                        return self.parse_binary_int_args("*")
                    case "-":
                        return self.parse_binary_int_args("-")
                    case "<":
                        return self.parse_binary_int_args("<")
                    case ">":
                        return self.parse_binary_int_args(">")
                    case "<=":
                        return self.parse_binary_int_args("<=")
                    case ">=":
                        return self.parse_binary_int_args(">=")
                    case "=":
                        return self.parse_binary_int_args("=")
                    case w:
                        raise NotImplementedError(f"Expression {w} not implemented.")

        return ast

    def peek(self) -> str:
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

    def peek_word(self) -> str:
        """
        Get word at the front of input string.

        Returns:
            str: Word at front of input string.
        """
        # Return no word if end of input has been reached.
        if self.pos == self.length:
            return ''

        # Return front word in input string.
        w = self.source[self.pos::].split(' ')[0]
        return w
    
    def skip_whitespace(self):
        """
        Removes leading whitespace in source code.
        """
        while self.peek() in WSP:
            self.pos += 1

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

        # Consume whitespace.
        self.skip_whitespace()

        # If not whitespace or end of input, number is of invalid format.
        #if self.peek() != '':
        #    raise TypeError("Invalid number type.")

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

        return "#\\" + ret_val

    def parse_unary_int_arg(self, exp_name: str) -> str:
        """
        Parses unary exression (exp_name e) with integer argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        self.pos += 1

        return exp

    def parse_unary_char_arg(self, exp_name: str) -> str:
        """
        Parses unary exression (exp_name e) with character argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse character or boolean and add to expression.
            case '#':
                # Skip over '#'.
                self.pos += 1
                arg = self.parse_char()
                exp.append(arg)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        self.pos += 1

        return exp

    def parse_unary_any_arg(self, exp_name: str) -> str:
        """
        Parses unary exression (exp_name e) with any type of argument from string.

        Returns:
            list: [exp_name, e].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that number follows.
        match self.peek():
            # Parse number and add to expression.
            case c if c.isdigit():
                num = self.parse_number()
                exp.append(num)
            # Parse character or boolean and add to expression.
            case '#':
                arg = self.parse_boolean_or_char()
                exp.append(arg)
            # Append nested expression to list of expression to list of expressions.
            case '(':
                exp.append(self.parse_expression())
            case _:
                raise TypeError(f"Invalid argument to {exp_name} expression.")
        
        # Consume whitespace.
        self.skip_whitespace()

        # If not closing parens, the expresion is invalid.
        if self.peek() != ')':
            raise TypeError(f"Invalid argument to {exp_name} expression.")

        # Skip closing parens.
        self.pos += 1

        return exp

    def parse_binary_int_args(self, exp_name: str) -> str:
        """
        Parses binary expression (exp_name e1 e2 ...) with integer arguments from string.

        Returns:
            list: [exp_name, e1, e2, ...].

        Raises:
            TypeError: Invalid expression.
        """
        exp = []

        # Skip over exp_name.
        self.pos += len(exp_name)

        exp.append(exp_name)

        # Consume whitespace.
        self.skip_whitespace()

        # Ensure that numbers follow and parse those numbers.
        while self.peek() != ')':
            match self.peek():
                # Parse number and add to expression.
                case c if c.isdigit():
                    num = self.parse_number()
                    exp.append(num)
                # Append nested expression to list of expression to list of expressions.
                case '(':
                    exp.append(self.parse_expression())
                case _:
                    raise TypeError(f"Invalid argument to {exp_name} expression.")
        
            # Consume whitespace.
            self.skip_whitespace()

        # Skip closing parens.
        self.pos += 1

        return exp


def scheme_parse(source: str) -> list:
    """
    Wrapper around parsing function for Scheme programs.

    Args:
        source (str): Scheme source program.

    Returns:
        list: Abstract syntax tree in the form of a Python list.
    """
    return Parser(source).parse()

if __name__ == "__main__":
    print(scheme_parse("   (+ 1 2 (+ 3 4) 5)   "))
