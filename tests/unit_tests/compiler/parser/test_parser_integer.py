# test_parser_integer.py - tests integer parsing
#
# Josh Meise
# 01-09-2026
# Description:
# - Tests parsig of single integers.
# - Ensures that whitespace is skipped.
# - Ensures that invlaid format integers are not accepted.
#

import unittest
import sys
import os
from compiler.parser import *

class IntegerParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of integers.
    """

    def _parse(self, source: str) -> int:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: Abstract syntax tree produced by parser.
        """
        return scheme_parse(source)

    def test_regular(self):
        """
        Test valid integer value.
        """
        self.assertEqual(self._parse("42"), 42)

    def test_leading_whitespace(self):
        """
        Tests valid integer value with leading whitespace.
        """
        self.assertEqual(self._parse("     42"), 42)

    def test_trailing_whitespace(self):
        """
        Tests valid integer with trailing whitespace.
        """
        self.assertEqual(self._parse("42   "), 42)

    def test_leading_trailing_whitespace(self):
        """
        Tests valid integer with both leading and trailing whitespace.
        """
        self.assertEqual(self._parse("    42   "), 42)

    def test_trailing_newline(self):
        """
        Tests valid integer with trailing newline.
        """
        self.assertEqual(self._parse("42\n"), 42)

    def test_eof_error(self):
        """
        Tests to make sure that RuntimeError is raised when provided with an empty string.
        """
        with self.assertRaises(RuntimeError):
            self._parse("")

    def test_invalid_int_0(self):
        """
        Test integer with invalid character in middle of integer.
        """
        with self.assertRaises(RuntimeError):
            self._parse("4i2")

    def test_invalid_int_1(self):
        """
        Test integer with invalid character in middle of integer.
        """
        with self.assertRaises(RuntimeError):
            self._parse("42i2")

    def test_invalid_int_2(self):
        """
        Test integer with invalid character at end of integer.
        """
        with self.assertRaises(RuntimeError):
            self._parse("42i")

    def test_invalid_int_3(self):
        """
        Test integer with invalid character at beginning of integer.
        """
        with self.assertRaises(RuntimeError):
            self._parse("i42")

if __name__ == '__main__':
    unittest.main()
