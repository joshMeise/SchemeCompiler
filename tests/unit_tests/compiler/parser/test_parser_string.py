# test_parser_string.py - tests (string "...") parsing
#
# Josh Meise
# 02-02-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class StringParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (string "...").
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["string", chars].
        """
        return scheme_parse(source)

    def test_string_regular(self):
        """
        Test (string "hi").
        """
        self.assertEqual(self._parse("(string \"hi\")"), ["string", "#\\h", "#\\i"])

    def test_string_regular_whitespace(self):
        """
        Test (string "hi") with whitespace.
        """
        self.assertEqual(self._parse("    (string    \"hi\")     "), ["string", "#\\h", "#\\i"])

    def test_string_regular_whitespace_middle(self):
        """
        Test (string "h i") with whitespace in middle of string.
        """
        self.assertEqual(self._parse("    (string \"h i\")     "), ["string", "#\\h", "#\\ ", "#\\i"])

    def test_string_regular_newline_middle(self):
        """
        Test (string "h\ni") with newline in middle of string.
        """
        self.assertEqual(self._parse("    (string \"h\ni\")     "), ["string", "#\\h", "#\\\n", "#\\i"])

    def test_string_no_closing_quote(self):
        """
        Test (string "hi).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(string \"hi)")

    def test_string_missing_parens(self):
        """
        Test (string "hi"
        """
        with self.assertRaises(RuntimeError):
            self._parse("(string \"hi\"")

if __name__ == '__main__':
    unittest.main()
