# integer.py - tests integer parsing
#
# Josh Meise
# 01-09-2026
# Description:
# - Tests parsig of single integers.
# - Ensures that whitespace is skipped.
# - Ensures that invlaid format integers are not accepted.
#
# TODO:
# - Maybe add multiple integers?
# - Add in tests of integers out of bounds (once bounds are determined).
#
# Questions:
# - Currently expcts a return of a list.
#

import unittest
import sys
import os
sys.path.append(os.path.abspath("../../../compiler/"))
from parser import Parser

class IntegerParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of integers.
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.
        """
        return Parser(source).parse()

    def test_regular(self):
        """
        Test valid integer value.
        """
        self.assertEqual(self._parse("42"), [42])

    def test_leading_whitespace(self):
        """
        Tests valid integer value with leading whitespace.
        """
        self.assertEqual(self._parse("     42"), [42])

    def test_trailing_whitespace(self):
        """
        Tests valid integer with trailing whitespace.
        """
        self.assertEqual(self._parse("42   "), [42])

    def test_leading_trailing_whitespace(self):
        """
        Tests valid integer with both leading and trailing whitespace.
        """
        self.assertEqual(self._parse("    42   "), [42])

    def test_eof_error(self):
        """
        Tests to make sure that EOFError is raised when provided with an empty string.
        """
        with self.assertRaises(EOFError):
            self._parse("")

    def test_invalid_int_0(self):
        """
        Test integer with invalid character in middle of integer.
        """
        with self.assertRaises(TypeError):
            self._parse("4i2")

    def test_invalid_int_1(self):
        """
        Test integer with invalid character in middle of integer.
        """
        with self.assertRaises(TypeError):
            self._parse("42i2")

    def test_invalid_int_2(self):
        """
        Test integer with invalid character at end of integer.
        """
        with self.assertRaises(TypeError):
            self._parse("42i")

if __name__ == '__main__':
    unittest.main()
