# test_parser_is_int.py - tests (integer? e) parsing
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
    Unit testing framework for the parsing of (integer? e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["integer?", integer].
        """
        return scheme_parse(source)

    def test_is_int_zero(self):
        """
        Test (integer? 0).
        """
        self.assertEqual(self._parse("(integer? 0)"), ["integer?", 0])

    def test_is_int_one_whitespace(self):
        """
        Test (integer? 1) with whitespace.
        """
        self.assertEqual(self._parse("    (integer?    1)     "), ["integer?", 1])

    def test_is_int_zero_invalid(self):
        """
        Test (integer? 0) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(integer? 0)a")

    def test_is_int_char(self):
        """
        Tests (integer? #\a).
        """
        self.assertEqual(self._parse("(integer? #\\a)"), ["integer?", "#\\a"])

    def test_is_int_bool(self):
        """
        Tests (integer? #t).
        """
        self.assertEqual(self._parse("(integer? #t)"), ["integer?", True])

if __name__ == '__main__':
    unittest.main()
