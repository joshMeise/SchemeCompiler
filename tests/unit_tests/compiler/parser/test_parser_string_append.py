# test_parser_string_append.py - tests (string-append (string "...") (string "...")) parsing
#
# Josh Meise
# 02-02-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class StringAppendParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (string-append (string "...") (string "...")).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["string", "..."].
        """
        return scheme_parse(source)

    def test_string_append_regular(self):
        """
        Test (string-append (string "hi") (string "ho")).
        """
        self.assertEqual(self._parse("(string-append (string \"hi\") (string \"ho\"))"), ["string-append", ["string", "\"hi\""], ["string", "\"ho\""]])

if __name__ == '__main__':
    unittest.main()
