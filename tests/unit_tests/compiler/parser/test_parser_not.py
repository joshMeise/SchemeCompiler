# test_parser_not.py - tests (not e) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class NotParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (not e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["not", integer].
        """
        return scheme_parse(source)

    def test_not_zero(self):
        """
        Test (not 0).
        """
        self.assertEqual(self._parse("(not 0)"), ["not", 0])

    def test_not_one_whitespace(self):
        """
        Test (not 1) with whitespace.
        """
        self.assertEqual(self._parse("    (not    1)     "), ["not", 1])

    def test_not_zero_invalid(self):
        """
        Test (not 0) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(not 0)a")

    def test_not_char(self):
        """
        Tests (not #\a).
        """
        self.assertEqual(self._parse("(not #\\a)"), ["not", "#\\a"])

    def test_not_bool(self):
        """
        Tests (not #t).
        """
        self.assertEqual(self._parse("(not #t)"), ["not", True])

if __name__ == '__main__':
    unittest.main()
