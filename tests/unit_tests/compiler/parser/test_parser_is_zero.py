# test_parser_is_zero.py - tests (zero? e) parsing
#
# Josh Meise
# 01-20-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import Parser

class IsZeroParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (zero? e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["zero?", integer].
        """
        return Parser(source).parse()

    def test_is_zero_zero(self):
        """
        Test (zero? 0).
        """
        self.assertEqual(self._parse("(zero? 0)"), ["zero?", 0])

    def test_is_zero_one_whitespace(self):
        """
        Test (zero? 1) with whitespace.
        """
        self.assertEqual(self._parse("    (zero?    1)     "), ["zero?", 1])

    def test_is_zero_zero_invalid(self):
        """
        Test (zero? 0) with trailing character.
        """
        with self.assertRaises(TypeError):
            self._parse("(zero? 0)a")

    def test_is_zero_char(self):
        """
        Tests (zero? #\a).
        """
        with self.assertRaises(TypeError):
            self._parse("(zero? #\\a)")

    def test_is_zero_bool(self):
        """
        Tests (zero? #t).
        """
        with self.assertRaises(TypeError):
            self._parse("(zero? #t)")

if __name__ == '__main__':
    unittest.main()
