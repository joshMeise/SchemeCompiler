# compiler.py - 
#
# Josh Meise
# 01-09-2026
# Description: 
#
# Citations:
# - ChatGPT for high level assistance on understanding of stack machines.
# - https://en.wikipedia.org/wiki/Stack_machine

import enum
from typing import BinaryIO

FIXNUM_SHIFT = 2
FIXNUM_TAG = 0
FIXNUM_MASK = 3
BOOL_SHIFT = 7
BOOL_TAG = 31
BOOL_MASK = 127
CHAR_SHIFT = 8
CHAR_TAG = 15
CHAR_MASK = 255
EMPTY_LIST_SHIFT = 8
EMPTY_LIST_TAG = 47
EMPTY_LIST_MASK = 255
VECTOR_SHIFT = 3
VECTOR_TAG = 2
VECTOR_MASK = 7
STRING_SHIFT = 3
STRING_TAG = 3
STRING_MASK = 7
SYMBOL_SHIFT = 3
SYMBOL_TAG = 5
SYMBOL_MASK = 7
CLOSURE_SHIFT = 3
CLOSURE_TAG = 6
CLOSURE_MASK = 7

UNARY_OPS = ["add1", "sub1", "integer->char", "char->integer", "null?", "zero?", "not", "integer?", "boolean?", "car", "cdr"]
BINARY_OPS = ["+", "*", "-", "<", ">", "<=", ">=", "=", "string-ref", "string-append", "vector-ref", "vector-append"]
TERNARY_OPS = ["string-set!", "vector-set!"]

class Compiler:
    """
    Class to handle the compilation of parsed Scheme programs.

    Will receive a list of parsed Scheme expressions from parser.
    
    Attributes:
        code (list): represents the current state of the stack
        max_locals_count (int):
    """

    def __init__(self):
        """
        Initializes the Compiler object.
        """
        self.code = []
        self.max_locals_count = 0

    def compile(self, expr, bindings: list):
        """
        Compiles given expression into bytecode.

        Args:
            expr: Expression to be compiled.
            bindings (list): Stack of binding environments.

        Raises:
            RuntimeError: Unbound variable name.
        """
        emit = self.code.append

        match expr:
            # Handle the case of the empty vector constructor.
            case "vector":
                emit(I.VEC)
                emit(0)
            case bool(_):
                emit(I.LOAD64)
                emit(box_bool(expr))
            case int(_):
                emit(I.LOAD64)
                emit(box_fixnum(expr))
            case str(s):
                match s[0]:
                    case "#":
                        emit(I.LOAD64)
                        emit(box_char(expr))
                    case _:
                        emit(I.GET_FROM_ENV)
                        if s not in bindings[-1]:
                            raise RuntimeError(f"Unbound variable {s}.")
                        emit(bindings[-1][s][0])
            case [only]:
                self.compile(only, bindings)
            case []:
                emit(I.LOAD64)
                emit(box_empty_list())
            # Compilation of an expression.
            case [first, *rest]:
                match first:
                    case w if w in BINARY_OPS:
                        self.compile(rest[0], bindings)
                        self.compile(rest[1], bindings)
                        self.emit_symbol(w)
                    case w if w in UNARY_OPS:
                        self.compile(rest[0], bindings)
                        self.emit_symbol(w)
                    case w if w in TERNARY_OPS:
                        self.compile(rest[0], bindings)
                        self.compile(rest[1], bindings)
                        self.compile(rest[2], bindings)
                        self.emit_symbol(w)
                    case w if w in ["string", "vector", "begin"]:
                        self.compile(rest, bindings)
                        self.emit_symbol(w)
                        emit(len(rest))
                    case "if":
                        self.compile(rest[0], bindings)
                        emit(I.POP_JUMP_IF_FALSE)
                        emit(get_len(rest[1]) + 2)
                        self.compile(rest[1], bindings)
                        emit(I.JUMP_OVER_ELSE)
                        emit(get_len(rest[2]))
                        self.compile(rest[2], bindings)
                    case "let":
                        # Compile bindings.
                        if len(bindings) == 0:
                            bindings.append({})
                        else:
                            bindings.append(bindings[-1].copy())
                        for i, binding in enumerate(rest[0]):
                            self.compile(rest[0][i][1], bindings[0:-1])
                            if binding[0] in bindings[-1]:
                                bindings[-1][binding[0]] = (new_val(bindings[-1]), bindings[-1][binding[0]][1] + 1)
                            else:
                                bindings[-1][binding[0]] = (new_val(bindings[-1]), 1)

                        emit(I.LET)
                        emit(len(rest[0]))
                        self.compile(rest[1], bindings)
                        bindings.pop()
                        emit(I.END_LET)
                    case "cons":
                        self.compile(rest[1], bindings)
                        self.compile(rest[0], bindings)
                        emit(I.CONS)
                    case "labels":
                        self.compile(rest[0], bindings)
                        self.compile(rest[1], bindings)
                    case "code":
                        emit(rest[1][0])
                        emit(get_len(rest[2]) + 1)
                        self.compile(rest[2], bindings)
                        emit(I.RET)
                    case "labelcall":
                        self.compile(rest[1], bindings)
                        emit(I.LABCALL)
                        emit(rest[0])
                    case _:
                        self.compile(first, bindings)
                        self.compile(rest, bindings)

    def compile_function(self, expr):
        """
        Compiles a given function into bytecode.

        Args:
            expr: Expression to be compiled.
        """
        self.compile(expr, [])
        self.code.append(I.RETURN)

    def write_to_stream(self, f: BinaryIO):
        """
        Writes instructions to file stream.

        Args:
            f (BinaryIO): File opened for writing in binary format.
        """
        for op in self.code:
            f.write(op.to_bytes(8, "little"))

    def emit_symbol(self, c: str):
        """
        Maps function names to their bytecode values.

        Args:
            c (str): Function name to be mapped.
        """
        emit = self.code.append
        match c:
            case "add1":
                emit(I.ADD1)
            case "sub1":
                emit(I.SUB1)
            case "integer->char":
                emit(I.INT_TO_CHAR)
            case "char->integer":
                emit(I.CHAR_TO_INT)
            case "null?":
                emit(I.IS_NULL)
            case "zero?":
                emit(I.IS_ZERO)
            case "not":
                emit(I.NOT)
            case "integer?":
                emit(I.IS_INT)
            case "boolean?":
                emit(I.IS_BOOL)
            case "+":
                emit(I.PLUS)
            case "*":
                emit(I.TIMES)
            case "-":
                emit(I.MINUS)
            case "<":
                emit(I.LT)
            case ">":
                emit(I.GT)
            case "<=":
                emit(I.LEQ)
            case ">=":
                emit(I.GEQ)
            case "=":
                emit(I.EQ)
            case "car":
                emit(I.CAR)
            case "cdr":
                emit(I.CDR)
            case "string":
                emit(I.STR)
            case "string-ref":
                emit(I.STR_REF)
            case "string-set!":
                emit(I.STR_SET)
            case "string-append":
                emit(I.STR_APP)
            case "vector":
                emit(I.VEC)
            case "vector-ref":
                emit(I.VEC_REF)
            case "vector-set!":
                emit(I.VEC_SET)
            case "vector-append":
                emit(I.VEC_APP)
            case "begin":
                emit(I.BEG)

def get_len(expr) -> int:
    """
    Compute bytecode length of a given expression.

    Args:
        expr: AST for expression.

    Returns:
        int: Number of instructions in expression's bytecode.
    """
    len = 0

    match expr:
        case c if (c in BINARY_OPS or c in UNARY_OPS):
            len += 1
        case "if":
            len += 4
        case bool(_):
            len += 2
        case int(_):
            len += 2
        case str(_):
            len += 2
        case []:
            len += 2
        case [only]:
            len += get_len(only)
        case [first, *rest]:
            len += get_len(first)
            len += get_len(rest)

    return len

def box_fixnum(val: int) -> int:
    """
    Implements pointer tagging scheme on integer values.
    Shifts 2 bits to the right and makes least significant 2 bits 0b00.
    
    Args:
        val (int): Integer vaue to be tagged.

    Returns:
        int: 64-bit tagged integer value.

    Raises:
        OverflowError: If integer value is larger than 2^62 - 1.
    """
    if val > 2**62 - 1:
        raise OverflowError("Integer value larger than 2^62 - 1.")

    return ((val << FIXNUM_SHIFT) & ~FIXNUM_MASK) | FIXNUM_TAG

def box_bool(val: bool) -> int:
    """
    Implements pointer tagging scheme on boolean values.
    True is 1 and false is 0.
    Shifts 7 bits to the right and makes least significant 7 bits 0b001111.
    
    Args:
        val (bool): Boolean value to be tagged.

    Returns:
        int: 64-bit tagged boolean value.
    """
    if val == True:
        return ((1 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG
    elif val == False:
        return ((0 << BOOL_SHIFT) & ~BOOL_MASK) | BOOL_TAG

def box_char(val: str) -> int:
    """
    Implements pointer tagging scheme on character values.
    Shifts 8 bits to the right and makes least significant 8 bits 0b00001111.
    
    Args:
        val (str): Character value to be tagged. In the form of <character>

    Returns:
        int: 64-bit tagged character value.
    """
    
    chr = val[-1]

    return ((ord(chr) << CHAR_SHIFT) & ~CHAR_MASK) | CHAR_TAG

def box_empty_list() -> int:
    """
    Implements pointer tagging scheme on empty list.
    Shifts 8 bits to the right and makes least significant 8 bits 0b00101111.
    
    Returns:
        int: 64-bit tagged list value.
    """

    return ((0 << EMPTY_LIST_SHIFT) & ~EMPTY_LIST_MASK) | EMPTY_LIST_TAG

def new_val(bindings: dict) -> int:
    """
    Gets runtime index for new binding from environment.

    Args:
        bindings (dict): Map of binding names to runtime index.

    Returns:
        int: Runtime index for new binding.
    """
    if bindings == {}:
        return 0

    tot = 0
    for val in bindings:
        tot += bindings[val][0]
    return tot + 1

class I(enum.IntEnum):
    """
    Class for the enumeration of all different opcodes.

    Starts at 1 and increments.
    """
    LOAD64 = enum.auto()
    RETURN = enum.auto()
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
    TIMES = enum.auto()
    MINUS = enum.auto()
    LT = enum.auto()
    GT = enum.auto()
    LEQ = enum.auto()
    GEQ = enum.auto()
    EQ = enum.auto()
    POP_JUMP_IF_FALSE = enum.auto()
    JUMP_OVER_ELSE = enum.auto()
    LET = enum.auto()
    GET_FROM_ENV = enum.auto()
    END_LET = enum.auto()
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
    LAB = enum.auto()
    CODE = enum.auto()
    LABCALL = enum.auto()
    GET_ARG =enum.auto()
    RET = enum.auto()
    CALL = enum.auto()

if __name__ == "__main__":
    compiler = Compiler()
    #compiler.compile_function(["labels", [["l0", ["code", [], [2], ["+", "a0", "a1"]]]], ["labelcall", 0, [4, 5]]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('a', 5)], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('a', ['let', [('a', 5)], ['a']])], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(["let", [("a", 4)], ['let', [('a', ['let', [('a', 4)], ['a']])], ['let', [('a', 5)], ['a']]]])
    #compiler.compile_function(['let', [('a', ['let', [('a', 5)], ['a']])], [['let', [('a', 6)], ['a']]]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('b', 1), ('a', ['let', [('a', 5)], ['b']])], [['let', [('a', 6)], ['a']]]]]])
    print(compiler.code)

