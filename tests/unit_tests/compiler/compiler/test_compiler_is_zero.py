# test_compiler_is_zero.py - tests compilation of (zero? e) expression
#
# Josh Meise
# 01-19-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import Compiler

class IsZeroCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (zero? e) expressions.
    """

    def _compile(self, expr: list) -> bytes:
        """
        Compiles the provided expression.
        Wrapper around Compile class' compile_function() and write_to_stream() functions.
        Writes compiled code to provided output stream.

        Args:
            expr (list): Expression to be compiled.
        
        Return:
            bytes: Bytes object containing compiled code.
        """
        buf = BytesIO()
        c = Compiler()
        c.compile_function(expr)
        c.write_to_stream(buf)
        return buf.getvalue()

    def test_is_zero_empty_list(self):
        """
        Tests (zero? ()).
        """
        self.assertEqual(self._compile(["zero?", []]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x2F\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_is_zero_0(self):
        """
        Tests (zero? 0).
        """
        self.assertEqual(self._compile(["zero?", 0]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
