# test_parser_letstar.py - tests parsing of letstar
#
# Josh Meise
# 03-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LetstarParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of letstar.
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

    def test_letstar_simple_1(self):
        """
        Test (letstar ((a 3) (b a) (c b)) c).
        """
        self.assertEqual(self._parse("(let* ((a 3) (b a) (c b)) c)"), ["let*", [("a", 3), ("b", Local("a")), ("c", Local("b"))], Local("c")])

    def test_letstar_simple_2(self):
        """
        Test (letstar ((a 3) (b a) (c a)) c).
        """
        self.assertEqual(self._parse("(let* ((a 3) (b a) (c a)) c)"), ["let*", [("a", 3), ("b", Local("a")), ("c", Local("a"))], Local("c")])

if __name__ == '__main__':
    unittest.main()
