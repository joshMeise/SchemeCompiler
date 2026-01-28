# test_parser_char_to_int.py - tests (char->integer e) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class CharToIntParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (char->integer e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["char->integer", integer].
        """
        return scheme_parse(source)

    def test_char_to_int_a(self):
        """
        Test (char->integer #\a).
        """
        self.assertEqual(self._parse("(char->integer #\\a)"), ["char->integer", "#\\a"])

    def test_char_to_int_a_whitespace(self):
        """
        Test (char->integer #\a) with whitespace.
        """
        self.assertEqual(self._parse("    (char->integer    #\\a)     "), ["char->integer", "#\\a"])

    def test_char_to_int_a_invalid(self):
        """
        Test (char->integer #\a) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(char->integer #\\a)a")

if __name__ == '__main__':
    unittest.main()
