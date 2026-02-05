# test_parser_is_null.py - tests (null? e) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class IsNullParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (null? e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["null?", integer].
        """
        return scheme_parse(source)

    def test_is_null_zero(self):
        """
        Test (null? 0).
        """
        self.assertEqual(self._parse("(null? 0)"), ["null?", 0])

    def test_is_null_one_whitespace(self):
        """
        Test (null? 1) with whitespace.
        """
        self.assertEqual(self._parse("    (null?    1)     "), ["null?", 1])

    def test_is_null_zero_invalid(self):
        """
        Test (null? 0) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(null? 0)a")

    def test_is_null_char(self):
        """
        Tests (null? #\a).
        """
        self.assertEqual(self._parse("(null? #\\a)"), ["null?", "#\\a"])

    def test_is_null_bool(self):
        """
        Tests (null? #t).
        """
        self.assertEqual(self._parse("(null? #t)"), ["null?", True])

if __name__ == '__main__':
    unittest.main()
