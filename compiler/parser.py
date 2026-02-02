# parser.py - 
#
# Josh Meise
# 01-30-2026
# Description: 
#
# Citations:
# - GeminiAI for re.DOTALL to get string to include newline.
#

import enum
import re

WSP = ['\n', '\r', '\t', ' ']

class Parser:
    """
    Class to handle parsing of Scheme program input text.

    Checks syntax of Scheme programs.
    Produces a list of tokens for use by compiler.

    Attributes:
        source (str): Scheme source program to be parsed.
        pos (int): Current position of parser in Scheme source program.
        length (int): Number of characters in Scheme program.
        text (str): Text corresponding to previously matched token.
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

    def get_token(self) -> Token:
        """
        Matches a token at the current position in the source code.
        Sets text to be matched value.

        Returns:
            Token: Matching token.

        Raises:
            RuntimeError: Text does not match an patterns.
        """
        # Consume whitespace.
        self.skip_whitespace()

        match self.source[self.pos:]:
            case _ if self.pos == self.length:
                self.text = "EOF"
                return Token.EOI
            case _ if t := re.match(r"\(", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.OP
            case _ if t := re.match(r"\)", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CP
            case _ if t := re.match(r"[0-9]+", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.INT
            case _ if t := re.match(r"#\\[^`]", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CHAR
            case _ if t := re.match(r"#[tfTF]", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.BOOL
            case _ if t := re.match(r"add1", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.ADD1
            case _ if t := re.match(r"sub1", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.SUB1
            case _ if t := re.match(r"integer\->char", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.INT_TO_CHAR
            case _ if t := re.match(r"char\->integer", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CHAR_TO_INT
            case _ if t := re.match(r"null\?", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.IS_NULL
            case _ if t := re.match(r"zero\?", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.IS_ZERO
            case _ if t := re.match(r"not", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.NOT
            case _ if t := re.match(r"integer\?", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.IS_INT
            case _ if t := re.match(r"boolean\?", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.IS_BOOL
            case _ if t := re.match(r"\+", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.PLUS
            case _ if t := re.match(r"\-", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.MINUS
            case _ if t := re.match(r"\*", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.TIMES
            case _ if t := re.match(r"<\=", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.LEQ
            case _ if t := re.match(r">\=", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.GEQ
            case _ if t := re.match(r"<", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.LT
            case _ if t := re.match(r">", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.GT
            case _ if t := re.match(r"<=", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.LEQ
            case _ if t := re.match(r">=", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.GEQ
            case _ if t := re.match(r"=", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.EQ
            case _ if t := re.match(r"if", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.IF
            case _ if t := re.match(r"cons", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CONS
            case _ if t := re.match(r"car", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CAR
            case _ if t := re.match(r"cdr", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.CDR
            case _ if t := re.match(r"string", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.STR
            case _:
                raise RuntimeError("Unrecognized token.")

    def match(self):
        """
        Consumes text in input stream.
        """
        self.pos += len(self.text)

    def skip_whitespace(self):
        """
        Removes leading whitespace in input stream.
        Allows parser to ignore whitespace.
        """
        while self.pos < self.length and self.source[self.pos] in WSP:
            self.pos += 1

    def get_identifier(self):
        """
        Matches a variable name in the input string.
        Sets text attribute to variable name.

        Raises:
            RuntimeError: Illegal identifier or end of input.
        """
        # Consume whitespace.
        self.skip_whitespace()

        match self.source[self.pos:]:
            case _ if self.pos == self.length:
                raise RuntimeError("Unexpected end of input.")
            case _ if t := re.match(r"[^(` \n\t\r1-9)]+", self.source[self.pos:]):
                self.text = t.group(0)
            case _:
                raise RuntimeError("Illegal identifier.")

    def get_string(self):
        """
        Matches a string literal in the input string.
        Sets text attribute to variable name.

        Raises:
            RuntimeError: String not found or end of input.
        """
        # Consume whitespace.
        self.skip_whitespace()

        match self.source[self.pos:]:
            case _ if self.pos == self.length:
                raise RuntimeError("Unexpected end of input.")
            case _ if t := re.match(r"\".*\"", self.source[self.pos:], re.DOTALL):
                self.text = t.group(0)
            case _:
                raise RuntimeError("String not found.")

    def parse(self) -> int | str | bool | list:
        """
        Parses expression from string.

        Returns:
            int | str | bool | list : AST containing expressions that have been parsed.

        Raises:
            RuntimeError: Unexpecteed token received.
        """
        match self.get_token():
            case Token.INT:
                ast = self.parse_int()
            case Token.CHAR:
                ast = self.parse_char()
            case Token.BOOL:
                ast = self.parse_bool()
            case Token.OP:
                ast = self.parse_expr()
            case _:
                raise RuntimeError(f"Unexpected token {self.text}")

        # Ensure end of input has been reached.
        if self.get_token() != Token.EOI:
            raise RuntimeError(f"Unexpected token {self.text}")

        return ast

    def parse_int(self) -> int:
        """
        Parses integer from string.

        Returns:
            int: Integer value that has been parsed.
        """
        # Convert to integer.
        val = int(self.text)

        # Consume text from input.
        self.match()

        return val

    def parse_char(self) -> str:
        """
        Parses character from string.

        Returns:
            str: Character value that has been parsed.
        """
        # Set text to character value (will be a string).
        val = self.text

        # Consume text from input.
        self.match()

        return val

    def parse_bool(self) -> bool:
        """
        Parses boolean from string.

        Returns:
            bool: Boolean value that has been parsed.
        """
        # Extract boolean value.
        if self.text in ["#t", "#T"]:
            val = True
        elif self.text in ["#f", "#F"]:
            val = False

        # Consume text from input.
        self.match()

        return val

    def parse_expr(self) -> list:
        """
        Parses Scheme function from string.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        ast = []

        # Consume opening parenthesis.
        self.match()

        match self.get_token():
            case _ if self.get_token() in [Token.ADD1, Token.SUB1, Token.INT_TO_CHAR, Token.CHAR_TO_INT, Token.IS_NULL, Token.IS_ZERO, Token.NOT, Token.IS_INT, Token.IS_BOOL, Token.CAR, Token.CDR]:
                ast = self.parse_unary()
            case _ if self.get_token() in [Token.PLUS, Token.MINUS, Token.TIMES, Token.LT, Token.GT, Token.LEQ, Token.GEQ, Token.EQ, Token.CONS]:
                ast = self.parse_binary()
            case Token.IF:
                ast = self.parse_ternary()
            case Token.CP:
                ast = []
            case Token.STR:
                ast = self.parse_string()
            case _:
                raise RuntimeError(f"Unexpected token {self.text}")

        # Consume closing parenthesis.
        if self.get_token() != Token.CP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        return ast

    def parse_unary(self) -> list:
        """
        Parses Scheme unary function from string.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        ast = [self.text]

        # Consume function name.
        self.match()

        match self.get_token():
            case Token.INT:
                ast.append(self.parse_int())
            case Token.CHAR:
                ast.append(self.parse_char())
            case Token.BOOL:
                ast.append(self.parse_bool())
            case Token.OP:
                ast.append(self.parse_expr())
            case _:
                raise RuntimeError(f"Unexpected token {self.text}")

        return ast

    def parse_binary(self) -> list:
        """
        Parses Scheme binary function from string.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        ast = [self.text]

        # Consume function name.
        self.match()

        i = 0
        while i < 2:
            match self.get_token():
                case Token.INT:
                    ast.append(self.parse_int())
                case Token.CHAR:
                    ast.append(self.parse_char())
                case Token.BOOL:
                    ast.append(self.parse_bool())
                case Token.OP:
                    ast.append(self.parse_expr())
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")
            i += 1

        return ast

    def parse_ternary(self) -> list:
        """
        Parses Scheme ternary function (such as an if statement) from string.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        ast = [self.text]

        # Consume function name.
        self.match()

        i = 0
        while i < 3:
            match self.get_token():
                case Token.INT:
                    ast.append(self.parse_int())
                case Token.CHAR:
                    ast.append(self.parse_char())
                case Token.BOOL:
                    ast.append(self.parse_bool())
                case Token.OP:
                    ast.append(self.parse_expr())
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")
            i += 1

        return ast

    def parse_string(self) -> list:
        """
        Parses Scheme string literal.

        Returns:
            list: String's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        ast = [self.text]

        # Consume function name.
        self.match()
        
        # Get string lietral from source.
        self.get_string()
        
        ast.append(self.text)

        # Consume string.
        self.match()

        return ast

#    def parse_let(self) -> list:
#        """
#        Parses let expression's bindings and expression.
#
#        Returns:
#            list: Expression's AST.
#
#        Raises:
#            RuntimeError: Unexpected token received or invalid binding.
#        """
#        # Consume "let".
#        self.match()
#
#        # Parse bindings where bindings list maps binding names to expressions.
#        bindings = {}
#
#        # Consume opening parenthesis.
#        if self.get_token() != Token.OP:
#            raise RuntimeError(f"Unexpected token {self.text}")
#        self.match()
#
#        while t := self.get_token() != Token.CP:
#            # Consume binding's opening parenthesis.
#            if t != Token.OP:
#                raise RuntimeError("Unexpected token {self.text}")
#            self.match()
#
#            # Get identifier.
#            self.get_identifier()
#
#            binding_name = self.text
#
#            self.match()
#
#            # Parse corresponding expression.
#            match self.get_token():
#                case Token.INT:
#                    expr = self.parse_int()
#                case Token.CHAR:
#                    expr = self.parse_char()
#                case Token.BOOL:
#                    expr = self.parse_bool()
#                case Token.OP:
#                    expr = self.parse_expr()
#                case _:
#                    raise RuntimeError(f"Unexpected token {self.text}")
#
#            # Consume closing parenthesis of binding.
#            if self.get_token() != Token.CP:
#                raise RuntimeError(f"Unexpected token {self.text}")
#            self.match()
#
#            # Ensure binding name is unique.
#            if binding_name in bindings:
#                raise RuntimeError(f"Repeat binding name detected {binding_name}")
#
#            # Add binding to bindings list.
#            bindings[binding_name] = expr
#
#        # Consume closing parenthesis of bindings.
#        self.match()
#
#        print(bindings)
#

class Token(enum.IntEnum):
    """
    Enumerates different token types.
    """
    OP = enum.auto()
    CP = enum.auto()
    EOI = enum.auto()
    INT = enum.auto()
    CHAR = enum.auto()
    BOOL = enum.auto()
    ADD1 = enum.auto()
    SUB1 = enum.auto()
    INT_TO_CHAR = enum.auto()
    CHAR_TO_INT = enum.auto()
    IS_NULL = enum.auto()
    IS_ZERO = enum.auto()
    NOT = enum.auto()
    IS_INT = enum.auto()
    IS_BOOL = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    TIMES = enum.auto()
    LT = enum.auto()
    GT = enum.auto()
    LEQ = enum.auto()
    GEQ = enum.auto()
    EQ = enum.auto()
    IF = enum.auto()
    LET = enum.auto()
    CONS = enum.auto()
    CAR = enum.auto()
    CDR = enum.auto()
    STR = enum.auto()

def scheme_parse(source: str) -> int | bool | str | list:
    """
    Wrapper around Parser class and parse() function.

    Returns:
        int | str | bool | list : AST containing expressions that have been parsed.
    """
    return Parser(source).parse()
