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
from collections import OrderedDict

WSP = ['\n', '\r', '\t', ' ']

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
    LET = enum.auto()
    ID = enum.auto()
    IF = enum.auto()
    CONS = enum.auto()
    CAR = enum.auto()
    CDR = enum.auto()
    STR = enum.auto()
    STR_REF = enum.auto()
    STR_SET = enum.auto()
    STR_APP = enum.auto()
    VEC = enum.auto()
    VEC_REF = enum.auto()
    VEC_SET = enum.auto()
    VEC_APP = enum.auto()
    BEG = enum.auto()
    LAMBDA = enum.auto()

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
            case _ if t := re.match(r"let", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.LET
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
            case _ if t := re.match(r"string\-ref", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.STR_REF
            case _ if t := re.match(r"string\-set\!", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.STR_SET
            case _ if t := re.match(r"string\-append", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.STR_APP
            case _ if t := re.match(r"string", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.STR
            case _ if t := re.match(r"vector\-ref", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.VEC_REF
            case _ if t := re.match(r"vector\-set\!", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.VEC_SET
            case _ if t := re.match(r"vector\-append", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.VEC_APP
            case _ if t := re.match(r"vector", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.VEC
            case _ if t := re.match(r"begin", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.BEG
            case _ if t := re.match(r"lambda", self.source[self.pos:]):
                self.text = t.group(0)
                return Token.LAMBDA
            case _ if not re.match(r"[^(` \n\t\r1-9#\(\))][^(` \n\t\r\(\))]*", self.source[self.pos:]):
                raise RuntimeError("Unrecognized token.")
            case _:
                self.get_identifier()
                return Token.ID

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
            case _ if t := re.match(r"[^(` \n\t\r1-9#)\(\)][^(` \n\t\r\(\))]*", self.source[self.pos:]):
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
            case _ if t := re.match(r"\"[^\"]*\"?", self.source[self.pos:], re.DOTALL):
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
                raise RuntimeError(f"Unexpected token {self.text}.")

        # Ensure end of input has been reached.
        if self.get_token() != Token.EOI:
            raise RuntimeError(f"Unexpected token {self.text}")

        print(ast)

        # Map binding names to indices.
        #ast = map_bindings(ast)

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

    def parse_binding(self, bindings: dict) -> str:
        """
        Parses binding from identifier.

        Args:
            bindings (dict): Map of identifers to indices in environment.

        Returns:
            str: 'b' concatenated with the binding index.

        Raises:
            RuntimeError: Identifier not in bindings list.
        """
        # Get identifier.
        self.get_identifier()
        id = self.text

        # Ensure identifier in bindings.
        if not id in bindings:
            raise RuntimeError(f"Unbound identifier {self.text}.")

        # Consume binding text.
        self.match()

        # Return binding index.
        return f"b{bindings[id]}"


    def parse_expr(self, in_let: bool = False) -> list:
        """
        Parses Scheme function from string.

        Args:
            bindings (dict): Map of bindings to indices.
            in_let (bool): Indicates whether or not to consider identifers as bindings.

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
                ast = self.parse_args(num_args = 1, in_let = in_let)
            case _ if self.get_token() in [Token.PLUS, Token.MINUS, Token.TIMES, Token.LT, Token.GT, Token.LEQ, Token.GEQ, Token.EQ, Token.CONS, Token.STR_REF, Token.STR_APP, Token.VEC_REF, Token.VEC_APP]:
                ast = self.parse_args(num_args = 2, in_let = in_let)
            case _ if self.get_token() in [Token.IF, Token.STR_SET, Token.VEC_SET]:
                ast = self.parse_args(num_args = 3, in_let = in_let)
            case _ if self.get_token() in [Token.VEC, Token.BEG]:
                ast = self.parse_args(num_args = -1, in_let = in_let)
            case Token.LET:
                ast = self.parse_let()
            case Token.LAMBDA:
                ast = self.parse_lambda()
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

    def parse_args(self, num_args: int = -1, in_let: bool = False) -> list:
        """
        Parses Scheme arguments function from string.

        Args:
            num_args (int): Number of arguments to parse, -1 means variable arity.
            bindings (dict): Map of bindings to indices.
            in_let (bool): Indicates whether or not to consider identifers as bindings.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        ast = [self.text]

        # Consume function name.
        self.match()

        # Parse arguments.
        n = 0
        while (num_args == -1 or n < num_args) and self.get_token() != Token.CP:
            match self.get_token():
                case Token.INT:
                    ast.append(self.parse_int())
                case Token.CHAR:
                    ast.append(self.parse_char())
                case Token.BOOL:
                    ast.append(self.parse_bool())
                case Token.OP:
                    ast.append(self.parse_expr(in_let = in_let))
                case _ if in_let and self.get_token() == Token.ID:
                    ast.append(self.text)
                    self.match()
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")

            n += 1

        # Ensure correct number of arguments parsed if not variable arity.
        if not num_args == -1 and n != num_args:
            raise RuntimeError(f"Incorrect number of arguments to {ast[0]}.")

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

        # Get string literal from source.
        self.get_string()

        for char in self.text[1:-1]:
            ast.append(f"#\\{char}")

        # Consume string.
        self.match()

        return ast

    def parse_let(self) -> list:
        """
        Parses let expression's bindings and expression.

        Returns:
            list: Expression's AST.
            bindings_ind (dict): Map of binding names to binding indices.

        Raises:
            RuntimeError: Unexpected token received or invalid binding.
        """
        # Insert function name.
        ast = [self.text]

        # Consume "let".
        self.match()

        # Parse bindings where bindings list maps binding names to expressions.
        bindings = OrderedDict()

        # Consume opening parenthesis.
        if self.get_token() != Token.OP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        while t := self.get_token() != Token.CP:
            # Consume binding's opening parenthesis.
            if t != Token.OP:
                raise RuntimeError("Unexpected token {self.text}")
            self.match()

            # Get identifier.
            self.get_identifier()
            binding_name = self.text
            self.match()

            # Parse corresponding expression.
            match self.get_token():
                case Token.INT:
                    expr = self.parse_int()
                case Token.CHAR:
                    expr = self.parse_char()
                case Token.BOOL:
                    expr = self.parse_bool()
                case Token.OP:
                    expr = self.parse_expr()
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")

            # Consume closing parenthesis of binding.
            if self.get_token() != Token.CP:
                raise RuntimeError(f"Unexpected token {self.text}")
            self.match()

            # Ensure binding name is unique.
            if binding_name in bindings:
                raise RuntimeError(f"Repeat binding name detected {binding_name}")

            # Add binding to bindings set.
            bindings[binding_name] =expr

        bindings_list = []
        for binding in bindings:
            bindings_list.append((binding, bindings[binding]))

        ast.append(bindings_list)

        # Consume closing parenthesis of bindings.
        self.match()

        # Parse expressions.
        expr_list = []
        while self.get_token() != Token.CP:
            match self.get_token():
                case Token.INT:
                    expr_list.append(self.parse_int())
                case Token.CHAR:
                    expr_list.append(self.parse_char())
                case Token.BOOL:
                    expr_list.append(self.parse_bool())
                case Token.OP:
                    expr_list.append(self.parse_expr(in_let = True))
                case Token.ID:
                    expr_list.append(self.text)
                    self.match()
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")

        # Append expression list to AST.
        ast.append(expr_list)

        return ast

    def parse_lambda(self) -> list:
        """
        Parses lambda expression from string.
        Form is (lambda (vars) body).
        Output is in closure form: (labels ((lvar (code (free_vars) (args) expr)) ...) (closure lvar args))

        Returns:
            list: String's AST.

        Raises:
            RuntimeError: Invalid labels syntax.
        """
        # Insert and consume "lambda".
        ast = [self.text]
        self.match()

        # Consume opening parenthesis.
        if self.get_token() != Token.OP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

#        # Map lvars to LExprs.
#        lvars = OrderedDict()
#
#        # Parse lvars.
#        while t := self.get_token() != Token.CP:
#            # Consume lvar's opening parenthesis.
#            if t != Token.OP:
#                raise RuntimeError("Unexpected token {self.text}")
#            self.match()
#
#            # Get identifier.
#            self.get_identifier()
#            lvar = self.text
#            self.match()
#            print(lvar)
#
#            lexpr = self.parse_lexpr()
#
#            # Consume closing parenthesis of lvar.
#            if self.get_token() != Token.CP:
#                raise RuntimeError(f"Unexpected token {self.text}")
#            self.match()
#
#            # Ensure lvar name is unique.
#            if lvar in lvars:
#                raise RuntimeError(f"Repeat lvar detected {lvar}")
#
#            # Add binding to bindings list.
#            lvars[lvar] = lexpr
#
#        print(lvars)
#
        # Consume closing parenthesis.
        if self.get_token() != Token.CP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        return ast

def map_bindings(ast: list, bindings: list = {}) -> list:
    if not bindings:
        bindings = {}

    if ast[0] == "let":
         # Map binding names to indices.
        for i, binding in enumerate(ast[1]):
            bindings[binding[0]] = new_val(bindings)
            ast[1][i] = binding[1]
            ast[2] = map_bindings(ast[2], bindings)
    elif type(ast[0]) == str:
        ast[0] = bindings[ast[0]]
    elif type(ast[0]) != int:
        for i, element in enumerate(ast):
            ast[i] = map_bindings(ast[i], bindings)

    return ast

def new_val(bindings: dict):
    if not bindings:
        return 0

    tot = 0
    for val in bindings:
        tot += bindings[val]

    return tot + 1

def scheme_parse(source: str) -> int | bool | str | list:
    """
    Wrapper around Parser class and parse() function.

    Returns:
        int | str | bool | list : AST containing expressions that have been parsed.
    """
    return Parser(source).parse()

if __name__ == "__main__":
    print(scheme_parse("(let ((a 4)) (let ((a 5)) (let ((a 6)) a)))"))
