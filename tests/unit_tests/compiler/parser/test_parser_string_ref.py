# test_parser_string_ref.py - tests (string_ref (string "...") e) parsing
#
# Josh Meise
# 02-01-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class StringRefParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (string_ref (string "...") e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["string-ref", ["string", "..."], e].
        """
        return scheme_parse(source)

    def test_string_ref_regular_1(self):
        """
        Test (string-ref (string "hi") 0).
        """
        self.assertEqual(self._parse("(string-ref (string \"hi\") 0)"), ["string-ref", ["string", "#\\h", "#\\i"], 0])

    def test_string_ref_regular_2(self):
        """
        Test (string-ref (string "hi") 1).
        """
        self.assertEqual(self._parse("(string-ref (string \"hi\") 1)"), ["string-ref", ["string", "#\\h", "#\\i"], 1])

if __name__ == '__main__':
    unittest.main()
