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
from .utils import *

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
        self.stack_ind = 0
        self.bindings = []

    def compile(self, expr, labels: dict, frees, bounds):
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
            case ["vector"]:
                self.stack_ind += 1
                emit(I.VEC)
                emit(0)
            case bool(_):
                self.stack_ind += 1
                emit(I.LOAD64)
                emit(box_bool(expr))
            case int(_):
                self.stack_ind += 1
                emit(I.LOAD64)
                emit(box_fixnum(expr))
            case s if type(expr) is Free:
                emit(I.GET_FREE)
                emit(frees.index(s.get_name()))
            case s if type(expr) is Bound:
                emit(I.GET_ARG)
                emit(bounds.index(s.get_name()))
            case str(s):
                match s[0]:
                    case "#":
                        self.stack_ind += 1
                        emit(I.LOAD64)
                        emit(box_char(expr))
                    case _:
                        self.stack_ind += 1
                        emit(I.PUSH_LET)
                        print(self.bindings)
                        if s not in self.bindings[-1]:
                            raise RuntimeError(f"Unbound variable {s}.")
                        emit(self.stack_ind - 1 - self.bindings[-1][s])
            case [only]:
                self.compile(only, labels, frees, bounds)
                emit(I.APPLY)
            case []:
                self.stack_ind += 1
                emit(I.LOAD64)
                emit(box_empty_list())
            # Compilation of an expression.
            case [first, *rest]:
                match first:
                    case w if w in BINARY_OPS:
                        self.compile(rest[0], labels, frees, bounds)
                        self.compile(rest[1], labels, frees, bounds)
                        self.emit_symbol(w)
                        self.stack_ind -= 1
                    case w if w in UNARY_OPS:
                        self.compile(rest[0], labels, frees, bounds)
                        self.emit_symbol(w)
                    case w if w in TERNARY_OPS:
                        self.compile(rest[0], labels, frees, bounds)
                        self.compile(rest[1], labels, frees, bounds)
                        self.compile(rest[2], labels, frees, bounds)
                        self.emit_symbol(w)
                        self.stack_ind -= 2
                    case w if w in ["string", "vector", "begin"]:
                        cnt = 0
                        for element in rest:
                            self.compile(element, labels, frees, bounds)
                            cnt += 1
                        self.emit_symbol(w)
                        emit(len(rest))
                        self.stack_ind -= (cnt - 1)
                    case "if":
                        self.compile(rest[0], labels, frees, bounds)
                        emit(I.POP_JUMP_IF_FALSE)
                        emit(get_len(rest[1]) + 2)
                        self.compile(rest[1], labels, frees, bounds)
                        emit(I.JUMP_OVER_ELSE)
                        emit(get_len(rest[2]))
                        self.compile(rest[2], labels, frees, bounds)
                    case "let":
                        # Compile bindings.
                        print("HERE")
                        if len(self.bindings) == 0:
                            self.bindings.append({})
                        else:
                            self.bindings.append(self.bindings[-1].copy())
                        for i, binding in enumerate(rest[0]):
                            print(f"compiling {rest[0][i][1]}")
                            print(self.bindings)
                            self.compile(rest[0][i][1], labels, frees, bounds)
                            if binding[0] in self.bindings[-1]:
                                self.bindings[-1][binding[0]] = self.stack_ind - 1
                            else:
                                self.bindings[-1][binding[0]] = self.stack_ind - 1

                        print(f"body compiling {rest[1]}")
                        self.compile(rest[1], labels, frees, bounds)
                        self.bindings.pop()
                        print(f"After pop {self.bindings}")
                        emit(I.END_LET)
                        emit(len(rest[0]))
                        self.stack_ind -= len(rest[0])
                    case "cons":
                        self.compile(rest[1], labels, frees, bounds)
                        self.compile(rest[0], labels, frees, bounds)
                        emit(I.CONS)
                        self.stack_ind -= 1
                    case "labels":
                        for element in rest[0]:
                            num = get_new_label_num(labels)
                            emit(I.LABEL)
                            emit(num)
                            labels[element[0]] = num
                            self.compile(element[1], labels, frees, bounds)
                        self.compile(rest[1], labels, frees, bounds)
                    case "code":
                        emit(len(rest[0]))
                        emit(len(rest[1]))
                        bounds = rest[0]
                        frees = rest[1]
                        emit(get_len(rest[2]) + 1)
                        self.compile(rest[2], labels, frees, bounds)
                        emit(I.RET)
                    case "closure":
                        emit(I.CLOSURE)
                        emit(labels[rest[0]])
                    case _:
                        self.compile(first, labels, frees, bounds)
                        self.compile(rest, labels, frees, bounds)

    def compile_function(self, expr):
        """
        Compiles a given function into bytecode.

        Args:
            expr: Expression to be compiled.
        """
        self.compile(expr, [], [], [])
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

def get_new_label_num(labels: dict) -> int:
    if labels == {}:
        return 0

    for i, (_, val) in enumerate(labels.items()):
        if i == 0:
            max = val
        elif i > max:
            max = i

    return max + 1

class I(enum.IntEnum):
    """
    Class for the enumeration of all different opcodes.

    Starts at 1 and increments.
    """
    LOAD64 = enum.auto()            # 0x01
    RETURN = enum.auto()            # 0x02
    ADD1 = enum.auto()              # 0x03
    SUB1 = enum.auto()              # 0x04
    INT_TO_CHAR = enum.auto()       # 0x05
    CHAR_TO_INT = enum.auto()       # 0x06
    IS_NULL = enum.auto()           # 0x07
    IS_ZERO = enum.auto()           # 0x08
    NOT = enum.auto()               # 0x09
    IS_INT = enum.auto()            # 0x0A
    IS_BOOL = enum.auto()           # 0x0B
    PLUS = enum.auto()              # 0x0C
    TIMES = enum.auto()             # 0x0D
    MINUS = enum.auto()             # 0x0E
    LT = enum.auto()                # 0x0F
    GT = enum.auto()                # 0x10
    LEQ = enum.auto()               # 0x11
    GEQ = enum.auto()               # 0x12
    EQ = enum.auto()                # 0x13
    POP_JUMP_IF_FALSE = enum.auto() # 0x14
    JUMP_OVER_ELSE = enum.auto()    # 0x15
    PUSH_LET = enum.auto()          # 0x16
    END_LET = enum.auto()           # 0x17
    CONS = enum.auto()              # 0x18
    CAR = enum.auto()               # 0x19
    CDR = enum.auto()               # 0x1A
    STR = enum.auto()               # 0x1B
    STR_REF = enum.auto()           # 0x1C
    STR_SET = enum.auto()           # 0x1D
    STR_APP = enum.auto()           # 0x1E
    VEC = enum.auto()               # 0x1F
    VEC_REF = enum.auto()           # 0x20
    VEC_SET = enum.auto()           # 0x21
    VEC_APP = enum.auto()           # 0x22
    BEG = enum.auto()               # 0x23
    LABEL = enum.auto()             # 0x24
    CODE = enum.auto()              # 0x25
    CLOSURE = enum.auto()           # 0x26
    GET_ARG = enum.auto()           # 0x27
    RET = enum.auto()               # 0x28
    APPLY = enum.auto()             # 0x29
    GET_FREE = enum.auto()          # 0x2A

if __name__ == "__main__":
    compiler = Compiler()
    #compiler.compile_function(["labels", [["l0", ["code", [], [2], ["+", "a0", "a1"]]]], ["labelcall", 0, [4, 5]]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('a', 5)], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('a', 5)], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(['let', [('a', ['let', [('a', 4)], 'a'])], 'a'])
    #compiler.compile_function(['let', [('a', 2), ('b', 3), ('c', 4), ('d', 5)], ['+', ['let', [('y', 6)], 'y'], ['+', ['let', [('y', 7)], 'y'],'b']]])
    #compiler.compile_function(['let', [('a', 4), ('b', 5)], ['+', 'a', 'b']])
    #compiler.compile_function(['let', [('a', 5)], ['let', [('b', 4)], ['-', 'a', 'b']]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('a', ['let', [('a', 5)], ['a']])], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(["let", [("a", 4)], ['let', [('a', ['let', [('a', 4)], ['a']])], ['let', [('a', 5)], ['a']]]])
    compiler.compile_function(['let', [('a', 4)], ['let', [('b', 4), ('a', ['let', [('a', 5)], 'b'])], ['let', [('a', 6)], 'a']]])
    #compiler.compile_function(['let', [('a', 4)], [['let', [('b', 1), ('a', ['let', [('a', 5)], ['b']])], [['let', [('a', 6)], ['a']]]]]])
    #compiler.compile_function(['let', [('a', 4)], ['+', 'a', 5]])
    #compiler.compile_function(['+', 4, 5])
    #compiler.compile_function(['begin', ['+', 4, 3]])
    #compiler.compile_function(["labels", [("f0", ["code", [], ["x", "y"], ["+", "x", "y"]])], ["closure", "f0", "x", "y"]])
    #compiler.compile_function(["labels", [("f0", ["code", [], ["x", "y"], ["+", Free("x"), Free("y")]]), ("f1", ["code", [], [], 3])], ["closure", "f0", "x", "y"]])
    #compiler.compile_function(['labels', [('f2', ['code', [], ['x', 'y'], ['+', Free("x"), Free("y")]])], [['let', [('x', 3), ('y', 4)], ['closure', 'f2', 'x', 'y']]]])
    print(compiler.code)

