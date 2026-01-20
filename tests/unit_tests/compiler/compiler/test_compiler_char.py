# test_compiler_char.py - tests character compiling
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

class CharacterCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of characters.
    """

    def _compile(self, expr: str) -> bytes:
        """
        Compiles the provided expression.
        Wrapper around Compile class' compile_function() and write_to_stream() functions.
        Writes compiled code to provided output stream.

        Args:
            expr (str): Character to be compiled.
        
        Return:
            bytes: Bytes object containing compiled code.
        """
        buf = BytesIO()
        c = Compiler()
        c.compile_function(expr)
        c.write_to_stream(buf)
        return buf.getvalue()

    def test_a(self):
        """
        Tests 'a'.
        """
        self.assertEqual(self._compile("#\\a"), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_A(self):
        """
        Tests 'A'.
        """
        self.assertEqual(self._compile("#\\A"), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x41\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_newline(self):
        """
        Tests newline.
        """
        self.assertEqual(self._compile("#\\\n"), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x0A\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

if __name__ == '__main__':
    unittest.main()
