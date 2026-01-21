# test_parser_int_to_char.py - tests (integer->char e) parsing
#
# Josh Meise
# 01-18-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import Parser

class IntToCharParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (integer->char e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["integer->char", integer].
        """
        return Parser(source).parse()

    def test_int_to_char_zero(self):
        """
        Test (integer->char 0).
        """
        self.assertEqual(self._parse("(integer->char 0)"), ["integer->char", 0])

    def test_int_to_char_one_whitespace(self):
        """
        Test (integer->char 1) with whitespace.
        """
        self.assertEqual(self._parse("    (integer->char    1)     "), ["integer->char", 1])

    def test_int_to_char_zero_invalid(self):
        """
        Test (integer->char 0) with trailing character.
        """
        with self.assertRaises(TypeError):
            self._parse("(integer->char 0)a")

    def test_int_to_char_char(self):
        """
        Tests (integer->char #\a).
        """
        with self.assertRaises(TypeError):
            self._parse("(integer->char #\\a)")

    def test_int_to_char_bool(self):
        """
        Tests (integer->char #t).
        """
        with self.assertRaises(TypeError):
            self._parse("(integer->char #t)")

if __name__ == '__main__':
    unittest.main()
