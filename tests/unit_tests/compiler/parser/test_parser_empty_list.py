# test_parser_empty_list.py - tests empty list parsing
#
# Josh Meise
# 01-18-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import Parser

class EmptyListParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of the empty list.
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: Empty list.
        """
        return Parser(source).parse()

    def test_empty_list(self):
        """
        Test regular empty list.
        """
        self.assertEqual(self._parse("()"), [])

    def test_invalid_empty_list(self):
        """
        Tests empty list with character following.
        """
        with self.assertRaises(TypeError):
            self._parse("()a")

if __name__ == '__main__':
    unittest.main()
