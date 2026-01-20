# test_compiler_int_to_char.py - tests compilation of (integer->char e)
#
# Josh Meise
# 01-20-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import Compiler

class IntToCharCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (integer->char e).
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

    def test_int_to_char_15(self):
        """
        Tests (integer->char 15).
        """
        self.assertEqual(self._compile(["integer->char", 15]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x3C\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_int_to_char_10(self):
        """
        Tests (integer->char 10).
        """
        self.assertEqual(self._compile(["integer->char", 10]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
