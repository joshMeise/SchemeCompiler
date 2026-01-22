# compiler.py - 
#
# Josh Meise
# 01-09-2026
# Description: 
#
# Questions:
# - Should expr be a list or a value?
#   - Thoughts are that compile takes an atomic value and compile_function takes a list (full parses expression).
# - What does env refer to in function signature for compile()?
#

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

UNARY_OPS = ["add1", "sub1", "integer->char", "char->integer", "null?", "zero?", "not", "integer?", "boolean?"]
BINARY_OPS = ["+", "*", "-", "<", ">", "<=", ">=", "="]

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

    def compile(self, expr):
        """
        Compiles given expression into bytecode.

        Args:
            expr: Expression to be compiled.
        """
        emit = self.code.append

        match expr:
            case bool(_):
                emit(I.LOAD64)
                emit(box_bool(expr))
            case int(_):
                emit(I.LOAD64)
                emit(box_fixnum(expr))
            case str(_):
                emit(I.LOAD64)
                emit(box_char(expr))
            case [only]:
                self.compile(only)
            case []:
                emit(I.LOAD64)
                emit(box_empty_list())
            # Compilation of an expression.
            case [first, *rest]:
                match first:
                    case o if o in BINARY_OPS:
                        self.compile(rest[0])
                        self.compile(rest[1])
                        self.emit_symbol(o)
                    case w if w in UNARY_OPS:
                        self.compile(rest[0])
                        self.emit_symbol(w)
                    case "if":
                        self.compile(rest[0])
                        emit(I.POP_JUMP_IF_FALSE)
                        emit(get_len(rest[1]) + 2)
                        self.compile(rest[1])
                        emit(I.JUMP_OVER_ELSE)
                        emit(get_len(rest[2]))
                        self.compile(rest[2])

    def compile_function(self, expr):
        """
        Compiles a given function into bytecode.

        Args:
            expr: Expression to be compiled.
        """
        self.compile(expr)
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

if __name__ == "__main__":
    compiler = Compiler()
    compiler.compile_function(["-", ["-", 4, 2], 1])
    print(compiler.code)

    compiler = Compiler()
    compiler.compile_function(["-", 5, ["-", 3, 1]])
    print(compiler.code)

    compiler = Compiler()
    compiler.compile_function(['+', ['+', 1 , ["+", 2, 3]], ["+", 4, 5]])
    print(compiler.code)

    compiler = Compiler()
    compiler.compile_function(['if', True, ['if', True, 4, 5], 6])
    print(compiler.code)

    compiler = Compiler()
    compiler.compile_function(['if', True, 6, ['if', True, 4, 5]])
    print(compiler.code)

    compiler = Compiler()
    compiler.compile_function(["if", ["if", True, True, False], ["if", True, 7, 8], ["if", True, 4, 5]])
    print(compiler.code)
