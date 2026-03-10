# test_parser_or.py - tests or parsing
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

class OrParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of or.
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

    def test_or_simple(self):
        """
        Test (or 1 4).
        """
        self.assertEqual(self._parse("(or 1 4)"), ["or", 1, 4])

if __name__ == '__main__':
    unittest.main()
