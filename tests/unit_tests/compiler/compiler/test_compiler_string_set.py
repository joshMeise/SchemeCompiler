# test_compiler_string_set.py - tests compilation of (string-set! (string "...") e e) expression
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

class StringSetCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (string-set! (string "...") e e) expressions.
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

    def test_string_set_regular_1(self):
        """
        Test (string-set! (string "hi") 0 a).
        """
        self.assertEqual(self._compile(["string-set!", ["string", "#\\h", "#\\i"], 0, "#\\a"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_string_set_regular_2(self):
        """
        Test (string-set! (string "hi") 1 b).
        """
        self.assertEqual(self._compile(["string-set!", ["string", "#\\h", "#\\i"], 1, "#\\b"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1C\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x62\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
