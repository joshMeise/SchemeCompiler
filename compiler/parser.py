# parser.py - 
#
# Josh Meise
# 01-30-2026
# Description: 
#
# Citations:
# - GeminiAI for re.DOTALL to get string to include newline.
#
# Uncertaities:
# Closure object is in double parens. IDK if this should be the case but I'm riding with it.
#

import enum
import re
from collections import OrderedDict
from .utils import *

WSP = ['\n', '\r', '\t', ' ']
BUILTINS = ["add1", "sub1", "integer->char", "char->integer", "null?", "zero?", "not", "integer?", "boolean?", "+", "-", "*", "<", ">", "<=", ">=", "=", "let", "if", "cons", "car", "cdr", "string-ref", "string-set!", "string-append", "string", "vector-ref", "vector-set!", "vector-append", "vector", "begin", "lambda", ]

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
        self.in_let = False
        self.insert_func_name = True
        self.in_lambda = False
        self.bound_vars = []

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

        ast = convert_to_closure(ast)

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

        Args:
            bindings (dict): Map of bindings to indices.

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
                ast = self.parse_args(num_args = 1)
            case _ if self.get_token() in [Token.PLUS, Token.MINUS, Token.TIMES, Token.LT, Token.GT, Token.LEQ, Token.GEQ, Token.EQ, Token.CONS, Token.STR_REF, Token.STR_APP, Token.VEC_REF, Token.VEC_APP]:
                ast = self.parse_args(num_args = 2)
            case _ if self.get_token() in [Token.IF, Token.STR_SET, Token.VEC_SET]:
                ast = self.parse_args(num_args = 3)
            case _ if self.get_token() in [Token.VEC, Token.BEG]:
                ast = self.parse_args(num_args = -1)
            case Token.LET:
                ast = self.parse_let()
            case Token.LAMBDA:
                ast = self.parse_lambda()
            case Token.CP:
                ast = []
            case Token.STR:
                ast = self.parse_string()
            case Token.OP:
                ast = self.parse_expr()
                self.insert_func_name = False
                ret = self.parse_args(num_args = -1)
                self.insert_func_name = True
                ast = [ast] + ret
            case _ if self.in_let and self.get_token() == Token.ID:
                ast = self.text
                self.match()
                self.insert_func_name = False
                ret = self.parse_args(num_args = -1)
                self.insert_func_name = True
                ast = [ast] +ret
            case _:
                raise RuntimeError(f"Unexpected token {self.text}")

        # Consume closing parenthesis.
        if self.get_token() != Token.CP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        return ast

    def parse_args(self, num_args: int = -1) -> list:
        """
        Parses Scheme arguments function from string.

        Args:
            num_args (int): Number of arguments to parse, -1 means variable arity.

        Returns:
            list: Expression's AST.

        Raises:
            RuntimeError: Unexpected token received.
        """
        # Insert function name.
        if self.insert_func_name:
            ast = [self.text]
            self.match()
        else:
            ast = []

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
                    ast.append(self.parse_expr())
                case _ if (self.in_let or self.in_lambda) and self.get_token() == Token.ID:
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
        self.in_let = True

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
                    expr_list.append(self.parse_expr())
                case Token.ID:
                    expr_list.append(self.text)
                    self.match()
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")

        if len(expr_list) == 0:
            raise RuntimeError("Missing body for let expression.")

        # Append expression list to AST.
        ast += expr_list

        self.in_let = False

        return ast

    def parse_lambda(self) -> list:
        """
        Parses lambda expression from string.
        Form is (lambda (vars) body).
        Output is in annotated lambda form: (lambda (bound_vars) (free_vars) expr)

        Returns:
            list: String's AST.

        Raises:
            RuntimeError: Invalid labels syntax.
        """
        self.in_lambda = True

        # Insert and consume "lambda".
        ast = [self.text]
        self.match()

        # Consume opening parenthesis.
        if self.get_token() != Token.OP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        self.bound_vars = []

        # Extract the names of the bound variables.
        while t := self.get_token() != Token.CP:
            # Get identifier.
            self.get_identifier()
            var = self.text
            self.match()

            if var in self.bound_vars:
                raise RuntimeError(f"Repeat bound variable detected {var}")

            self.bound_vars.append(var)

        # Consume closing parenthesis.
        if self.get_token() != Token.CP:
            raise RuntimeError(f"Unexpected token {self.text}")
        self.match()

        # Parse body.
        while self.get_token() != Token.CP:
            match self.get_token():
                case Token.INT:
                    expr = self.parse_int()
                case Token.CHAR:
                    expr = self.parse_char()
                case Token.BOOL:
                    expr = self.parse_bool()
                case Token.OP:
                    expr = self.parse_expr()
                case Token.ID:
                    expr = self.text
                    self.match()
                case _:
                    raise RuntimeError(f"Unexpected token {self.text}")

        # Lift free variables from expression.
        free_vars = get_free_vars(self.bound_vars, expr)
 
        ast.append(self.bound_vars)
        ast.append(free_vars)
        ast.append(expr)

        self.in_lambda = False

        return ast

def get_closure_form(lambda_body, cur_count):
    return ["closure", f"f{cur_count}"] + lambda_body

def convert_to_closure_helper(ast: list, labels, cur_count, new_ast = []) -> list:
    match ast:
        case [only]:
            return [convert_to_closure_helper(only, labels, cur_count, new_ast)]
        case [first, *rest]:
            if first == "lambda":
                labels[f"f{cur_count}"] = [rest[0], rest[1], convert_to_closure_helper(rest[2], labels, cur_count + 1)]
                return get_closure_form(rest[1], cur_count)
            elif first == "let":
                ret_val = [first]
                bindings = []
                for element in rest[0]:
                    bindings.append((element[0], convert_to_closure_helper(element[1], labels, cur_count, new_ast)))
                    cur_count += 1
                ret_val.append(bindings)
                ret_val.append(convert_to_closure_helper(rest[1], labels, cur_count, new_ast))
                return ret_val
            else:
                ret_val = [convert_to_closure_helper(first, labels, cur_count, new_ast)]
                ret_val += convert_to_closure_helper(rest, labels, cur_count, new_ast)
                return ret_val
        case int(_):
            return ast
        case str(_):
            return ast
        case []:
            return ast
        case _:
            raise NotImplementedError("Not yet implemented")

def convert_to_closure(ast: list) -> list:
    labels = {}

    body = convert_to_closure_helper(ast, labels, 0)

    if len(labels) != 0:
        for name, code in labels.items():
            code[2] = annotate_free_vars(code[1], code[2])
            code[2] = annotate_bound_vars(code[0], code[2])
        labels = [(name, ["code"] + code) for name, code in labels.items()]
        body = annotate_locals(body, [])
        return ["labels", labels] + [body]
    else:
        ast = annotate_locals(ast, [])
        return ast

def get_free_vars_helper(bound_vars, expr, free_vars):
    match expr:
        case str(_) if expr not in bound_vars and expr not in BUILTINS and expr[0] != '#':
            free_vars.append(expr)
        case [only]:
            get_free_vars_helper(bound_vars, only, free_vars)
        case [first, *rest]:
            get_free_vars_helper(bound_vars, first, free_vars)
            get_free_vars_helper(bound_vars, rest, free_vars)

def get_free_vars(bound_vars, expr):
    free_vars = []

    get_free_vars_helper(bound_vars, expr, free_vars)

    # Remove duplicates.
    free_vars_dict = dict.fromkeys(free_vars, None)
    free_vars = [var for var in free_vars_dict]

    return free_vars

def annotate_free_vars(free_vars, expr):
    match expr:
        case _ if type(expr) is str and expr in free_vars:
            return Free(expr)
        case [first, *rest]:
            return [annotate_free_vars(free_vars, first), *[annotate_free_vars(free_vars, r) for r in rest]]
        case _:
            return expr

def annotate_bound_vars(bound_vars, expr):
    match expr:
        case _ if type(expr) is str and expr in bound_vars:
            return Bound(expr)
        case [first, *rest]:
            return [annotate_bound_vars(bound_vars, first), *[annotate_bound_vars(bound_vars, r) for r in rest]]
        case _:
            return expr

def annotate_locals(expr: list, locals: list):
    match expr:
        case _ if len(locals) != 0 and type(expr) is str and expr in locals[-1]:
            return Local(expr)
        case [first, *rest]:
            if first == "let":
                # Add all bound locals to set.
                if len(locals) != 0:
                    locals.append(locals[-1])
                else:
                    locals = [set()]
                new_bindings = [(b[0], annotate_locals(b[1], locals)) for b in rest[0]]
                for binding in rest[0]:
                    locals[-1].add(binding[0])
                ret_val = [first, new_bindings, annotate_locals(rest[1], locals)]
                locals.pop()
                return ret_val
            else:
                return [annotate_locals(first, locals), *[annotate_locals(r, locals) for r in rest]]
        case _:
            return expr

def scheme_parse(source: str) -> int | bool | str | list:
    """
    Wrapper around Parser class and parse() function.

    Returns:
        int | str | bool | list : AST containing expressions that have been parsed.
    """
    return Parser(source).parse()

if __name__ == "__main__":
    #print(scheme_parse("(let ((a 4) (b 5)) (+ a b))"))
    #print(scheme_parse("(let ((a 5) (b (let ((c 4)) c))) (+ a b))"))
    #print(scheme_parse("(let ((a (let ((b 4)) b))) (let ((c 5)) c))"))
    #print(scheme_parse("(let ((a 4)) (let ((a (let ((a 5)) a))) (let ((a 6)) a)))"))
    #print(scheme_parse("(let ((a (let ((a 5)) a))) (let ((a 6)) a))"))
    #print(scheme_parse("(let ((a 4)) (let ((b 4) (a (let ((a 5)) b))) (let ((a 6)) a)))"))
    #print(scheme_parse("(let ((a 4)) (let ((a 5)) (let ((a 6)) a)))"))
    #print(scheme_parse("(lambda (x y) (lambda () (+ x y)))"))
    #print(scheme_parse("(let ((x 5)) (lambda (y) (lambda () (+ x y))))"))
    #print(scheme_parse("(lambda () (+ x y))"))
    #print(scheme_parse("(lambda (x) (+ x y))"))
    #print(scheme_parse("(lambda (x y) (+ x y))"))
    #print(scheme_parse("((lambda (x) (+ x y)) (+ 4 5))"))
    print(scheme_parse("(let ((b (let ((a 4)) a))) b)"))
    #print(scheme_parse("(let ((x 2) (y 3)) (+ (let ((y 4)) y) y))"))
    #print(scheme_parse("((let ((x 2)) (lambda () (+ x 3))) 4)"))
    #print(scheme_parse("((let ((x 3) (y 4)) (lambda () (+ x y))))"))
    #print(scheme_parse("(+ 4 5)"))
    #print(scheme_parse("((+ 4 5))"))
    #print(scheme_parse("(let ((x 4) (y 5)) (lambda () (+ x y)))"))
    #print(scheme_parse("(let ((x 4)) (+ x 4))"))
    #print(scheme_parse("(lambda (y) (+ x y))"))
    #print(scheme_parse("((lambda () 3))"))
    #print(scheme_parse("(+ ((lambda () 3)) 4)"))
    #print(scheme_parse("(let ((b 2)) (let ((a (lambda (y) (+ y b)))) (+ (a 1) (a 1))))"))
    #print(scheme_parse("(let ((a ((lambda () 4))) (b ((lambda () 3)))) (+ a b))"))
    #print(scheme_parse("(let ((x 3)) (lambda (y) y))"))
