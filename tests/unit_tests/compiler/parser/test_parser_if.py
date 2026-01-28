# test_parser_if.py - tests (if test conseq altern)  parsing
#
# Josh Meise
# 01-22-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class IfParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (if test conseq altern).
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
        return scheme_parse(source)

    def test_plain_if(self):
        """
        Test (if #t 3 4).
        """
        self.assertEqual(self._parse("(if #t 3 4)"), ["if", True, 3, 4])

    def test_nested_test_if(self):
        """
        Test (if (if #t #t #f) 5 4).
        """
        self.assertEqual(self._parse("(if (if #t #t #f) 5 4)"), ["if", ["if", True, True, False], 5, 4])

    def test_nested_conseq_if(self):
        """
        Test (if #t (if #f 5 6) 4).
        """
        self.assertEqual(self._parse("(if #t (if #f 5 6) 4)"), ["if", True, ["if", False, 5, 6], 4])
    
    def test_nested_altern_if(self):
        """
        Test (if #t 4 (if #f 5 6)).
        """
        self.assertEqual(self._parse("(if #t 4 (if #f 5 6))"), ["if", True, 4, ["if", False, 5, 6]])

if __name__ == '__main__':
    unittest.main()
