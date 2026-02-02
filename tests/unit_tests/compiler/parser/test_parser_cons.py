# test_parser_cons.py - tests (cons e1 e2) parsing
#
# Josh Meise
# 02/01-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class ConsParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (cons e1 e2).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["cons", e1, e2].
        """
        return scheme_parse(source)

    def test_cons_zero_args(self):
        """
        Test (cons).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons)")

    def test_cons_one_arg(self):
        """
        Test (cons 1).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons 1)")

    def test_cons_two_args(self):
        """
        Test (cons 1 2).
        """
        self.assertEqual(self._parse("(cons 1 2)"), ["cons", 1, 2])

    def test_cons_two_args_whitespace(self):
        """
        Test (cons 1 2) with whitespace.
        """
        self.assertEqual(self._parse("    (   cons   1    2   )     "), ["cons", 1, 2])

    def test_cons_two_args_invalid(self):
        """
        Test (cons 1 2) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons 1 2)a")

    def test_cons_three_args(self):
        """
        Tests (cons 1 2 3)..
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons 1 2 3)")

    def test_cons_first_nested(self):
        """
        Tests (cons (cons 1 2) 3).
        """
        self.assertEqual(self._parse("(cons (cons 1 2) 3)"), ["cons", ["cons", 1, 2], 3])

    def test_cons_second_nested(self):
        """
        Tests (cons 1 (cons 2 3)).
        """
        self.assertEqual(self._parse("(cons 1 (cons 2 3))"), ["cons", 1, ["cons", 2, 3]])

    def test_cons_both_nested(self):
        """
        Tests (cons (cons 1 2) (cons 3 4)).
        """
        self.assertEqual(self._parse("(cons (cons 1 2) (cons 3 4))"), ["cons", ["cons", 1, 2], ["cons", 3, 4]])

    def test_cons_both_nested_three_args(self):
        """
        Tests (cons (cons 1 2) (cons 3 4) 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons (cons 1 2) (cons 3 4) 5)")

    def test_cons_first_nested_three_args(self):
        """
        Tests (cons (cons 1 2) 3 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons (cons 1 2) 3 5)")

    def test_cons_second_nested_three_args(self):
        """
        Tests (cons 1 (cons 2 3) 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons 1 (cons 2 3) 5)")

    def test_cons_no_closing_parens(self):
        """
        Tests (cons 1 2.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(cons 1 2")

if __name__ == '__main__':
    unittest.main()
