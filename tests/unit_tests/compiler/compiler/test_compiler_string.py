# test_compiler_string.py - tests compilation of (string "...") expression
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

class StringCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (string "...") expressions.
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

    def test_string_regular(self):
        """
        Test (string "hi").
        """
        self.assertEqual(self._compile(["string", "#\\h", "#\\i"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_string_newline(self):
        """
        Test (string "h\ni").
        """
        self.assertEqual(self._compile(["string", "#\\h", "#\\\n", "#\\i"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x0A\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
