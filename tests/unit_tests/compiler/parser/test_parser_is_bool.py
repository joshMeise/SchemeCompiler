# test_parser_is_bool.py - tests (boolean? e) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class IsIntParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (boolean? e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["boolean?", integer].
        """
        return scheme_parse(source)

    def test_is_bool_zero(self):
        """
        Test (boolean? 0).
        """
        self.assertEqual(self._parse("(boolean? 0)"), ["boolean?", 0])

    def test_is_bool_one_whitespace(self):
        """
        Test (boolean? 1) with whitespace.
        """
        self.assertEqual(self._parse("    (boolean?    1)     "), ["boolean?", 1])

    def test_is_bool_zero_invalid(self):
        """
        Test (boolean? 0) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(boolean? 0)a")

    def test_is_bool_char(self):
        """
        Tests (boolean? #\a).
        """
        self.assertEqual(self._parse("(boolean? #\\a)"), ["boolean?", "#\\a"])

    def test_is_bool_bool(self):
        """
        Tests (boolean? #t).
        """
        self.assertEqual(self._parse("(boolean? #t)"), ["boolean?", True])

if __name__ == '__main__':
    unittest.main()
