# test_parser_labmda.py - tests lambda parsing
#
# Josh Meise
# 02-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LambdaParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of lambda expressions.
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: closure form of lambda expression
        """
        return scheme_parse(source)

    def test_lambda_one_bound(self):
        """
        Test (lambda (x) x).
        """
        self.assertEqual(self._parse("(lambda (x) x)"), ["labels", [("f0", ["code", ["x"], [], Bound("x")])], ["closure", "f0"]])

    def test_lambda_one_bound_one_free(self):
        """
        Test (lambda (y) (+ x y)).
        """
        self.assertEqual(self._parse("(lambda (y) (+ x y))"), ["labels", [("f0", ["code", ["y"], ["x"], ["+", Free("x"), Bound("y")]])], ["closure", "f0", "x"]])

    def test_lambda_one_free(self):
        """
        Test (lambda () x).
        """
        self.assertEqual(self._parse("(lambda () x)"), ["labels", [("f0", ["code", [], ["x"], Free("x")])], ["closure", "f0", "x"]])

    def test_lambda_two_free(self):
        """
        Test (lambda () (+ x y)).
        """
        self.assertEqual(self._parse("(lambda () (+ x y))"), ["labels", [("f0", ["code", [], ["x", "y"], ["+", Free("x"), Free("y")]])], ["closure", "f0", "x", "y"]])

    def test_lambda_with_let_bound(self):
        """
        Test (let ((x 3)) (lambda (y) y)).
        """
        self.assertEqual(self._parse("(let ((x 3)) (lambda (y) y))"), ["labels", [("f1", ["code", ["y"], [], Bound("y")])], ["let", [("x", 3)], ["closure", "f1"]]])

    def test_lambda_called_no_arg(self):
        """
        Test ((lambda () 3)).
        """
        self.assertEqual(self._parse("((lambda () 3))"), ["labels", [("f0", ["code", [], [], 3])], [["closure", "f0"]]])

    def test_lambda_called_one_arg(self):
        """
        Test ((lambda (x) (+ x 3)) 4).
        """
        self.assertEqual(self._parse("((lambda (x) (+ x 3)) 4)"), ["labels", [("f0", ["code", ["x"], [], ["+", Bound("x"), 3]])], [["closure", "f0"], 4]])

    def test_lambda_two_bindings(self):
        """
        Test (let ((a ((lambda () 4))) (b ((lambda () 3)))) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a ((lambda () 4))) (b ((lambda () 3)))) (+ a b))"), ["labels", [("f0", ["code", [], [], 4]), ("f1", ["code", [], [], 3])], ['let', [('a', [['closure', 'f0']]), ('b', [['closure', 'f1']])], ['+', Local('a'), Local('b')]]])

if __name__ == '__main__':
    unittest.main()
