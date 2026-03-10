# test_parser_quote.py - tests complex constant parsing
#
# Josh Meise
# 02-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class QuoteParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of complex constants.
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

    def test_quote_one_symbol_1(self):
        """
        Test (quote a).
        """
        self.assertEqual(self._parse("(quote a)"), ["labels", [("t0", ["constant-init", ["symbol", "a"]])], ["constant-ref", "t0"]])

    def test_quote_one_symbol_2(self):
        """
        Test (quote (a b)).
        """
        self.assertEqual(self._parse("(quote (a b))"), ["labels", [("t0", ["constant-init", ["symbol", "(", "a", "b", ")"]])], ["constant-ref", "t0"]])

    def test_quote_one_vector(self):
        """
        Test (quote #(1 2)).
        """
        self.assertEqual(self._parse("(quote #(1 2))"), ["labels", [("t0", ["constant-init", ["vector", 1, 2]])], ["constant-ref", "t0"]])

    def test_quote_one_vector_symbols(self):
        """
        Test (quote #(a b)).
        """
        self.assertEqual(self._parse("(quote #(a b))"), ["labels", [("t0", ["constant-init", ["vector", ["symbol", "a"], ["symbol", "b"]]])], ["constant-ref", "t0"]])

    def test_quote_in_let(self):
        """
        Test (let ((a (quote #(1 2)))) a).
        """
        self.assertEqual(self._parse("(let ((a (quote #(1 2)))) a)"), ["labels", [("t0", ["constant-init", ["vector", 1, 2]])], ["let", [("a", ["constant-ref", "t0"])], Local("a")]])

    def test_quote_in_lambda(self):
        """
        Test (lambda () (quote #(1 2)))
        """
        self.assertEqual(self._parse("(lambda () (quote #(1 2)))"), ["labels", [("t1", ["constant-init", ["vector", 1, 2]]), ("f0", ["code", [], [], ["constant-ref", "t1"]])], ["closure", "f0"]])



if __name__ == '__main__':
    unittest.main()
