# test_parser_begin.py - tests (begin e1 e2 ...) parsing
#
# Josh Meise
# 02-04-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class BeginParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (begin e1 e2 ...).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["begin", e1, e2, ...].
        """
        return scheme_parse(source)

    def test_begin_one_exp(self):
        """
        Test (begin (string "hi")).
        """
        self.assertEqual(self._parse("(begin (string \"hi\"))"), ["begin", ["string", "#\\h", "#\\i"]])

    def test_begin_two_exp(self):
        """
        Test (begin (string "hi") (+ 4 3)).
        """
        self.assertEqual(self._parse("(begin (string \"hi\") (+ 4 3))"), ["begin", ["string", "#\\h", "#\\i"], ["+", 4 , 3]])

    def test_begin_three_exp(self):
        """
        Test (begin #t #f #t).
        """
        self.assertEqual(self._parse("(begin #t #f #t)"), ["begin", True, False, True])

    def test_begin_four_exp(self):
        """
        Test (begin (string "hi") (- 4 3) a ()).
        """
        self.assertEqual(self._parse("(begin (string \"hi\") (- 4 3) #\\a ())"), ["begin", ["string", "#\\h", "#\\i"], ["-", 4, 3], "#\\a", []])

if __name__ == '__main__':
    unittest.main()
