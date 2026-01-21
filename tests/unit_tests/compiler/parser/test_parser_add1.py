# test_parser_add1.py - tests (add1 e) parsing
#
# Josh Meise
# 01-18-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import Parser

class Add1ParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (add1 e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["add1", integer].
        """
        return Parser(source).parse()

    def test_add1_zero(self):
        """
        Test (add1 0).
        """
        self.assertEqual(self._parse("(add1 0)"), ["add1", 0])

    def test_add1_one_whitespace(self):
        """
        Test (add1 1) with whitespace.
        """
        self.assertEqual(self._parse("    (add1    1)     "), ["add1", 1])

    def test_add1_zero_invalid(self):
        """
        Test (add1 0) with trailing character.
        """
        with self.assertRaises(TypeError):
            self._parse("(add1 0)a")

    def test_add1_char(self):
        """
        Tests (add1 #\a).
        """
        with self.assertRaises(TypeError):
            self._parse("(add1 #\\a)")

    def test_add1_bool(self):
        """
        Tests (add1 #t).
        """
        with self.assertRaises(TypeError):
            self._parse("(add1 #t)")

    def test_add1_nested(self):
        """
        Test (add1 (add1 0)).
        """
        self.assertEqual(self._parse("(add1 (add1 0))"), ["add1", ["add1", 0]])

    def test_add1_double_nested(self):
        """
        Test (add1 (add1 (add1 0))).
        """
        self.assertEqual(self._parse("(add1 (add1 (add1 0)))"), ["add1", ["add1", ["add1", 0]]])
        
    def test_add1_missing_parens(self):
        """
        Test (add1 0
        """
        with self.assertRaises(TypeError):
            self._parse("(add1 0")

if __name__ == '__main__':
    unittest.main()
