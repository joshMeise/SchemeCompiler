# test_parser_string_set.py - tests (string_set! (string "...") e e) parsing
#
# Josh Meise
# 02-01-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class StringSetParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (string_set! (string "...") e e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["string-set!", ["string", "..."], e, e].
        """
        return scheme_parse(source)

    def test_string_set_regular_1(self):
        """
        Test (string-set! (string "hi") 0 a).
        """
        self.assertEqual(self._parse("(string-set! (string \"hi\") 0 #\\a)"), ["string-set!", ["string", "#\\h", "#\\i"], 0, "#\\a"])

    def test_string_ref_regular_2(self):
        """
        Test (string-set! (string "hio") 1, b).
        """
        self.assertEqual(self._parse("(string-set! (string \"hio\") 1 #\\b)"), ["string-set!", ["string", "#\\h", "#\\i", "#\\o"], 1, "#\\b"])

if __name__ == '__main__':
    unittest.main()
