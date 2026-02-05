# test_parser_car.py - tests (car (cons e1 e2)) parsing
#
# Josh Meise
# 01-18-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class CarParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (car (cons e1 e2)).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["car", ["cons", e1, e2]].
        """
        return scheme_parse(source)

    def test_car_simple(self):
        """
        Test (car (cons 1 3)).
        """
        self.assertEqual(self._parse("(car (cons 1 3))"), ["car", ["cons", 1, 3]])

    def test_car_nested_cons_1(self):
        """
        Test (car (cons (cons 1 2) 3)).
        """
        self.assertEqual(self._parse("(car (cons (cons 1 2) 3))"), ["car", ["cons", ["cons", 1, 2], 3]])

    def test_car_nested_cons_2(self):
        """
        Test (car (cons 3 (cons 1 2))).
        """
        self.assertEqual(self._parse("(car (cons 3 (cons 1 2)))"), ["car", ["cons", 3, ["cons", 1, 2]]])

    def test_car_missing_parens(self):
        """
        Test (car (cons 3 4)
        """
        with self.assertRaises(RuntimeError):
            self._parse("(car (cons 3 4)")

    def test_car_two_expr(self):
        """
        Test (car (cons 3 4) 3)
        """
        with self.assertRaises(RuntimeError):
            self._parse("(car (cons 3 4) 3)")

if __name__ == '__main__':
    unittest.main()
