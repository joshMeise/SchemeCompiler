# test_parser_sub1.py - tests (sub1 e) parsing
#
# Josh Meise
# 01-21-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class Sdd1ParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (sub1 e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["sub1", integer].
        """
        return scheme_parse(source)

    def test_sub1_zero(self):
        """
        Test (sub1 0).
        """
        self.assertEqual(self._parse("(sub1 0)"), ["sub1", 0])

    def test_sub1_one_whitespace(self):
        """
        Test (sub1 1) with whitespace.
        """
        self.assertEqual(self._parse("    (sub1    1)     "), ["sub1", 1])

    def test_sub1_zero_invalid(self):
        """
        Test (sub1 0) with trailing character.
        """
        with self.assertRaises(RuntimeError):
            self._parse("(sub1 0)a")

if __name__ == '__main__':
    unittest.main()
