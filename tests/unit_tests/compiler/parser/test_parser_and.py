# test_parser_and.py - tests and parsing
#
# Josh Meise
# 03-10-2026
# Description:
# - Tests parsing of true and fasle values.
#

import unittest
import sys
import os
from compiler.parser import *

class AndParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of and.
    """

    def _parse(self, source: str) -> bool:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            bool: Boolean value parsed by function.
        """
        return scheme_parse(source)

    def test_and_simple(self):
        """
        Test (and 1 4).
        """
        self.assertEqual(self._parse("(and 1 4)"), ["and", 1, 4])

if __name__ == '__main__':
    unittest.main()
