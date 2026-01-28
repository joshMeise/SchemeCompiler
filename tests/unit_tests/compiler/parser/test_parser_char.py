# test_parser_char.py - tests character parsing
#
# Josh Meise
# 01-19-2026
# Description:
# - Tests parsing of character values.
#

import unittest
import sys
import os
from compiler.parser import *

class CharacterParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of characters.
    """

    def _parse(self, source: str) -> str:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            str: Character value parsed by function.
        """
        return scheme_parse(source)

    def test_a(self):
        """
        Test 'a'.
        """
        self.assertEqual(self._parse("#\\a"), '#\\a')

    def test_A(self):
        """
        Test 'A'.
        """
        self.assertEqual(self._parse("#\\A"), '#\\A')

    def test_newline(self):
        """
        Test '\n'.
        """
        self.assertEqual(self._parse("#\\\n"), '#\\\n')

    def test_double_quote(self):
        """
        Test '"'.
        """
        self.assertEqual(self._parse("#\\\""), '#\\\"')

    def test_illegal(self):
        """
        Test '`'.
        """
        with self.assertRaises(RuntimeError):
            self._parse("#\\`")

    def test_no_hash(self):
        """
        Test no piund sign.
        """
        with self.assertRaises(RuntimeError):
            self._parse("\\a")

    def test_no_backslash(self):
        """
        Test no backslash.
        """
        with self.assertRaises(RuntimeError):
            self._parse("#a")

    def test_string(self):
        """
        Test more than one character after backslash.
        """
        with self.assertRaises(RuntimeError):
            self._parse("#\\ab")

if __name__ == '__main__':
    unittest.main()
