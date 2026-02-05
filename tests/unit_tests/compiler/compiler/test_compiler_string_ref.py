# test_compiler_string_ref.py - tests compilation of (string-ref (string "...") e) expression
#
# Josh Meise
# 02-02-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import Compiler

class StringRefCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (string-ref (string "...") e) expressions.
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

    def test_string_ref_regular_1(self):
        """
        Test (string-ref (string "hi") 0).
        """
        self.assertEqual(self._compile(["string-ref", ["string", "#\\h", "#\\i"], 0]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_string_ref_regular_2(self):
        """
        Test (string-ref (string "hi") 1).
        """
        self.assertEqual(self._compile(["string-ref", ["string", "#\\h", "#\\i"], 1]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x1D\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
