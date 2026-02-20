# test_compiler_string_append.py - tests compilation of (string-append (string "...") (string "...")) expression
#
# Josh Meise
# 02-03-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import Compiler

class StringRefCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (string-append (string "...") (string "...")) expressions.
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

    def test_string_append_regular(self):
        """
        Test (string-append (string "hi") (string "ho")).
        """
        self.assertEqual(self._compile(["string-append", ["string", "#\\h", "#\\i"], ["string", "#\\h", "#\\o"]]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x69\x00\x00\x00\x00\x00\x00\x1B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x68\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x6F\x00\x00\x00\x00\x00\x00\x1B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
