# test_compiler_char_to_int.py - tests compilation of (char->integer e)
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

class CharToIntCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of (char->integer e).
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

    def test_char_to_int_a(self):
        """
        Tests (char->integer #\a).
        """
        self.assertEqual(self._compile(["char->integer", "#\\a"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_char_to_int_newline(self):
        """
        Tests (char->integer #\\n).
        """
        self.assertEqual(self._compile(["char->integer", "#\\\n"]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x0A\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
