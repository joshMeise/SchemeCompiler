# test_compiler_letstar.py - tests compilation of letstar
#
# Josh Meise
# 03-01-2026
# Description:
#

from io import BytesIO
import unittest
import sys
import os
from compiler.compiler import *

class LetstarCompileTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of letstar.
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

    def test_letstar_simple_1(self):
        """
        Test (let* ((a 3) (b a) (c b)) c).
        """
        self.assertEqual(self._compile(["let*", [("a", 3), ("b", Local("a")), ("c", Local("b"))], Local("c")]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_letstar_simple_2(self):
        """
        Test (let* ((a 3) (b a) (c a)) c).
        """
        self.assertEqual(self._compile(["let*", [("a", 3), ("b", Local("a")), ("c", Local("a"))], Local("c")]), b"\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_letstar_invalid(self):
        """
        Test (let* ((a b) (b 3) (c a)) c)
        """
        with self.assertRaises(RuntimeError):
            self._compile(["let*", [("a", "b"), ("b", 3), ("c", Local("a"))], Local("c")])

if __name__ == '__main__':
    unittest.main()
