# test_parser_vector_append.py - tests (vector-append (vector e1 e2 ...) (vector e1 e2 ...)) parsing
#
# Josh Meise
# 02-03-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class VectorAppendParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (vector-append (vector e1 e2 ...) (vector e1 e2 ...)).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["vector-append", ["vector", e1, e2, ...], ["vector", e1, e2, ...]].
        """
        return scheme_parse(source)

    def test_vector_append_regular(self):
        """
        Test (vector-append (vector 1 3 4) (vector 2 3 #t)).
        """
        self.assertEqual(self._parse("(vector-append (vector 1 3 4) (vector 2 3 #t))"), ["vector-append", ["vector", 1, 3, 4], ["vector", 2, 3, True]])

if __name__ == '__main__':
    unittest.main()
