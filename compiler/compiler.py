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
            expr (): expression to be compiled.
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
    
    def compile_function(self, expr):
        """

        Args:
            
        """
        self.compile(expr)
        self.code.append(I.RETURN)

    def write_to_stream(self, f: BinaryIO):
        """
        Writes instructions to file stream.

        Args:
            f (BinaryIO): File opened for writing in binrayr format.
        """
        for op in self.code:
            f.write(op.to_bytes(8, "little"))

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
        val (str): Character value to be tagged.

    Returns:
        int: 64-bit tagged character value.
    """

    return ((ord(val) << CHAR_SHIFT) & ~CHAR_MASK) | CHAR_TAG

class I(enum.IntEnum):
    """
    Class for the enumeration of all different opcodes.

    Starts at 1 and increments.
    """
    LOAD64 = enum.auto()
    RETURN = enum.auto()

