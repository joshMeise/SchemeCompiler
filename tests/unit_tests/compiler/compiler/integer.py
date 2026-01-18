# integer.py - tests integer compiling
#
# Josh Meise
# 01-09-2026
# Description:
#
# Questions:
# - Currently expcts an input of just a single integer.
# - Currently calls compile_function() (with just an integer and not a list) instead of compile().
# - Does bounds checking need to be tested here since it will be enforced by the parser?
#   - Currently testing bounds checking by just seeing if value overflows.
#   - This is caught by an OverflowError..
#

from io import BytesIO
import unittest
import sys
import os
sys.path.append(os.path.abspath("../../../../compiler"))
from compiler import Compiler

class IntegerParseTests(unittest.TestCase):
    """
    Unit testing framework for the compiling of integers.
    """

    def _compile(self, expr: int) -> bytes:
        """
        Compiles the provided expression.
        Wrapper around Compile class' compile_function() and write_to_stream() functions.
        Writes compiled code to provided output stream.

        Args:
            expr (int): Integer to be compiled.
        
        Return:
            bytes: Bytes object containing compiled code.
        """
        buf = BytesIO()
        c = Compiler()
        c.compile_function(expr)
        c.write_to_stream(buf)
        return buf.getvalue()

    def test_zero(self):
        """
        Tests zero as an integer value.
        """
        self.assertEqual(self._compile(0), b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_one(self):
        """
        Tests one as an integer value.
        """
        self.assertEqual(self._compile(1), b"\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_max_val(self):
        """
        Tests 2^62-1 as an integer value.
        """
        self.assertEqual(self._compile(2**62 - 1), b"\x01\x00\x00\x00\x00\x00\x00\x00\xFC\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x02\x00\x00\x00\x00\x00\x00\x00")

    def test_max_val_plus_one(self):
        """
        Tests 2^62 as an integer value.
        Tests for overflow error.
        """
        with self.assertRaises(OverflowError):
            self._compile(2**62)

if __name__ == '__main__':
    unittest.main()
