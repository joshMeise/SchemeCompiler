# parser.py - 
#
# Josh Meise
# 01-30-2026
# Description: 
#

import enum
import re

WSP = ['\n', '\r', '\t', ' ']

class Parser:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.length = len(source)

    def get_token(self) -> Token:
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
            case _:
                raise RuntimeError("Unrecognized token.")

    def match(self):
        """
        Consumes text in source code moving pointer forward.
        """
        self.pos += len(self.text)


    def skip_whitespace(self):
        """
        Removes leading whitespace in source code.
        """
        while self.pos < self.length and self.source[self.pos] in WSP:
            self.pos += 1

    def parse(self):
        """
        Parses input strings of various objects.

        Returns:
            Atomic element or abstract syntax tree in the form of a Python list.

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
        # Convert to integer.
        val = int(self.text)

        # Consume text from input.
        self.match()

        return val

    def parse_char(self) -> str:
        # Set text to character value (will be a string).
        val = self.text

        # Consume text from input.
        self.match()

        return val

    def parse_bool(self) -> bool:
        # Extract boolean value.
        if self.text in ["#t", "#T"]:
            val = True
        elif self.text in ["#f", "#F"]:
            val = False

        # Consume text from input.
        self.match()

        return val

    def parse_expr(self) -> list:
        ast = []

        # Consume opening parenthesis.
        self.match()

        match self.get_token():
            case _ if self.get_token() in [Token.ADD1, Token.SUB1, Token.INT_TO_CHAR, Token.CHAR_TO_INT, Token.IS_NULL, Token.IS_ZERO, Token.NOT, Token.IS_INT, Token.IS_BOOL]:
                ast = self.parse_unary()
            case _ if self.get_token() in [Token.PLUS, Token.MINUS, Token.TIMES, Token.LT, Token.GT, Token.LEQ, Token.GEQ, Token.EQ]:
                ast = self.parse_binary()
            case Token.IF:
                ast = self.parse_ternary()
            case Token.CP:
                ast = []
            case _:
                raise RuntimeError(f"Unexpected token {self.text}")

        # Consume closing parenthesis.
        if self.get_token() != Token.CP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        return ast

    def parse_unary(self) -> list:
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

    def parse_ternary(self) -> list:
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


class Token(enum.IntEnum):
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

def scheme_parse(source: str) -> object:
    return Parser(source).parse()
