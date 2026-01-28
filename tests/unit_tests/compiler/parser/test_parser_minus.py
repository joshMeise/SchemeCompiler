# test_parser_minus.py - tests (- e1 e2) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class MinusParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (- e1 e2).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["-", e1, e2].
        """
        return scheme_parse(source)

    def test_minus_zero_args(self):
        """
        Test (-).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(-)")

    def test_minus_one_arg(self):
        """
        Test (- 1).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- 1)")

    def test_minus_two_args(self):
        """
        Test (- 1 2).
        """
        self.assertEqual(self._parse("(- 1 2)"), ["-", 1, 2])

    def test_minus_two_args_whitespace(self):
        """
        Test (- 1 2) with whitespace.
        """
        self.assertEqual(self._parse("    (   -   1    2   )     "), ["-", 1, 2])

    def test_minus_two_args_invalid(self):
        """
        Test (- 1 2) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- 1 2)a")

    def test_minus_three_args(self):
        """
        Tests (- 1 2 3)..
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- 1 2 3)")

    def test_minus_first_nested(self):
        """
        Tests (- (- 1 2) 3).
        """
        self.assertEqual(self._parse("(- (- 1 2) 3)"), ["-", ["-", 1, 2], 3])

    def test_minus_second_nested(self):
        """
        Tests (- 1 (- 2 3)).
        """
        self.assertEqual(self._parse("(- 1 (- 2 3))"), ["-", 1, ["-", 2, 3]])

    def test_minus_both_nested(self):
        """
        Tests (- (- 1 2) (- 3 4)).
        """
        self.assertEqual(self._parse("(- (- 1 2) (- 3 4))"), ["-", ["-", 1, 2], ["-", 3, 4]])

    def test_minus_both_nested_three_args(self):
        """
        Tests (- (- 1 2) (- 3 4) 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- (- 1 2) (- 3 4) 5)")

    def test_minus_first_nested_three_args(self):
        """
        Tests (- (- 1 2) 3 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- (- 1 2) 3 5)")

    def test_minus_second_nested_three_args(self):
        """
        Tests (- 1 (- 2 3) 5).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- 1 (- 2 3) 5)")

    def test_minus_no_closing_parens(self):
        """
        Tests (- 1 2.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(- 1 2")

if __name__ == '__main__':
    unittest.main()
