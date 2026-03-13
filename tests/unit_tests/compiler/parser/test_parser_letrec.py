# test_parser_letrec.py - tests parsing of letrec
#
# Josh Meise
# 03-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LetrecParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of letrec.
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

    def test_letrec_simple(self):
        """
        Test (letrec ((even? (lambda (n) (if (= 0 n) #t (odd? (- n 1))))) (odd? (lambda (n) (if (= 0 n) #f (even? (- n 1)))))) (even? 88)).
        """
        self.assertEqual(self._parse("(letrec ((even? (lambda (n) (if (= 0 n) #t (odd? (- n 1))))) (odd? (lambda (n) (if (= 0 n) #f (even? (- n 1)))))) (even? 88))"), ["labels", [("f1", ["code", ["n"], ["odd?"], ["if", ["=", 0, Bound("n")], True, [Free("odd?"), ["-", Bound("n"), 1]]]]), ("f2", ["code", ["n"], ["even?"], ["if", ["=", 0, Bound("n")], False, [Free("even?"), ["-", Bound("n"), 1]]]])], ["letrec", [("even?", ["closure", "f1", Local("odd?")]), ("odd?", ["closure", "f2", Local("even?")])], [Local("even?"), 88]]])

if __name__ == '__main__':
    unittest.main()
