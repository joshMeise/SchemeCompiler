# compiler.py - 
#
# Josh Meise
# 01-09-2026
# Description: 
#

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

    def compile(self, expr, env):
        """

        Args:
            
        """
        emit = self.code.append
        match expr:
            case int(_):
                emit(I.LOAD64)
                emit(box_fixnum(expr))

    def compile_function(self, expr):
        """

        Args:
            
        """
        self.compile(expr)
        self.code.append(I.RETURN)


class I(enum.IntEnum):
    """
    Class for the enumeration of all different opcodes.

    """
    LOAD64 = enum.auto()
    RETURN = enum.auto()
