# test_parser_vector_ref.py - tests (vector_ref (vector e1 e2 ...) e) parsing
#
# Josh Meise
# 02-01-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class VectorRefParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (vector_ref (vector e1 e2 ...) e).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["vector-ref", ["vector", e1, e2, ...], e].
        """
        return scheme_parse(source)

    def test_vector_ref_regular_1(self):
        """
        Test (vector-ref (vector (string "hi")) 0).
        """
        self.assertEqual(self._parse("(vector-ref (vector (string \"hi\")) 0)"), ["vector-ref", ["vector", ["string", "\"hi\""]], 0])

    def test_vector_ref_regular_2(self):
        """
        Test (vector-ref (vector 1 2) 1).
        """
        self.assertEqual(self._parse("(vector-ref (vector 1 2) 1)"), ["vector-ref", ["vector", 1, 2], 1])

if __name__ == '__main__':
    unittest.main()
