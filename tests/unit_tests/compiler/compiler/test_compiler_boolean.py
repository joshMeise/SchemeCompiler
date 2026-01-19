# test_compiler_boolean.py - tests boolean compiling
#
# Josh Meise
# 01-09-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import Compiler

class BooleanCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of boolean.
    """

    def _compile(self, expr: bool) -> bytes:
        """
        Compiles the provided expression.
        Wrapper around Compile class' compile_function() and write_to_stream() functions.
        Writes compiled code to provided output stream.

        Args:
            expr (bool): Boolean to be compiled.
        
        Return:
            bytes: Bytes object containing compiled code.
        """
        buf = BytesIO()
        c = Compiler()
        c.compile_function(expr)
        c.write_to_stream(buf)
        return buf.getvalue()

    def test_true(self):
        """
        Tests true compile.
        """
        self.assertEqual(self._compile(True), b"\x01\x00\x00\x00\x00\x00\x00\x00\x9F\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_false(self):
        """
        Tests false compile.
        """
        self.assertEqual(self._compile(False), b"\x01\x00\x00\x00\x00\x00\x00\x00\x1F\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
