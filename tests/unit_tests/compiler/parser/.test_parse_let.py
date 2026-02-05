# test_parser_let.py - tests (let bindings body)  parsing
#
# Josh Meise
# 01-22-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import Parser

class LetParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (let bindings body).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["if", test, conseq, altern]
        """
        return Parser(source).parse()

    def test_let_one_binding_unused(self):
        """
        Test (let ((a 4)) 3).
        """
        self.assertEqual(self._parse("(let ((a 4)) 3)"), [4, ["let", 1, 3]])
    
    def test_let_one_binding_used(self):
        """
        Test (let ((a 4)) a).
        """
        self.assertEqual(self._parse("(let ((a 4)) a)"), [4, ["let", 1, "b0"]])

    def test_let_two_bindings_first_used(self):
        """
        Test (let ((a 4) (b 5)) a).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) a)"), [4, 5, ["let", 2, "b0"]])

    def test_let_two_bindings_second_used(self):
        """
        Test (let ((a 4) (b 5)) b).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) b)"), [4, 5, ["let", 2, "b1"]])

    def test_let_two_bindings_both_used(self):
        """
        Test (let ((a 4) (b 5)) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) (+ a b))"), [4, 5, ["let", 2, ["+", "b0", "b1"]]])

if __name__ == '__main__':
    unittest.main()
