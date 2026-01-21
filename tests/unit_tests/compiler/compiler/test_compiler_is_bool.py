# test_compiler_is_bool.py - tests compilation of (boolean? e) expression
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

class IsBoolCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (boolean? e) expressions.
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

    def test_is_bool_regular(self):
        """
        Test (boolean? #t).
        """
        self.assertEqual(self._compile(["boolean?", True]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x9f\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_is_bool_nested(self):
        """
        Test (boolean? (boolean? 1)).
        """
        self.assertEqual(self._compile(["boolean?", ["boolean?", 1]]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_is_bool_double_nested(self):
        """
        Test (boolean? (boolean? (boolean? #\a))).
        """
        self.assertEqual(self._compile(["boolean?", ["boolean?", ["boolean?", "#\\a"]]]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
