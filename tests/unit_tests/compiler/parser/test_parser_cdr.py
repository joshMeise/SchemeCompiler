# test_parser_cdr.py - tests (cdr (cons e1 e2)) parsing
#
# Josh Meise
# 02-01-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class CdrParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (cdr (cons e1 e2)).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["cdr", ["cons", e1, e2]].
        """
        return scheme_parse(source)

    def test_cdr_simple(self):
        """
        Test (cdr (cons 1 3)).
        """
        self.assertEqual(self._parse("(cdr (cons 1 3))"), ["cdr", ["cons", 1, 3]])

    def test_cdr_nested_cons_1(self):
        """
        Test (cdr (cons (cons 1 2) 3)).
        """
        self.assertEqual(self._parse("(cdr (cons (cons 1 2) 3))"), ["cdr", ["cons", ["cons", 1, 2], 3]])

    def test_cdr_nested_cons_2(self):
        """
        Test (cdr (cons 3 (cons 1 2))).
        """
        self.assertEqual(self._parse("(cdr (cons 3 (cons 1 2)))"), ["cdr", ["cons", 3, ["cons", 1, 2]]])

    def test_cdr_missing_parens(self):
        """
        Test (cdr (cons 3 4)
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cdr (cons 3 4)")

    def test_cdr_two_expr(self):
        """
        Test (cdr (cons 3 4) 3)
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cdr (cons 3 4) 3)")

if __name__ == '__main__':
    unittest.main()
