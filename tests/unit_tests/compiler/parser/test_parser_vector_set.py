# test_parser_vector_set.py - tests (vector_set! (vector e1 e2 ...) e e) parsing
#
# Josh Meise
# 02-03-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class VectorSetParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (vector_set! (vector e1 e2 ...) e e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["vector-set!", ["vector", e1, e2, ...], e, e].
        """
        return scheme_parse(source)

    def test_vector_set_regular_1(self):
        """
        Test (vector-set! (vector 1) 0 a).
        """
        self.assertEqual(self._parse("(vector-set! (vector 1) 0 #\\a)"), ["vector-set!", ["vector", 1], 0, "#\\a"])

    def test_vector_ref_regular_2(self):
        """
        Test (vector-set! (vector 2 #t a) 1, b).
        """
        self.assertEqual(self._parse("(vector-set! (vector 2 #t #\\a) 1 #\\b)"), ["vector-set!", ["vector", 2, True, "#\\a"], 1, "#\\b"])

if __name__ == '__main__':
    unittest.main()
