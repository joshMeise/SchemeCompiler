# test_parser_vector.py - tests (vector e1 e2 ...) parsing
#
# Josh Meise
# 02-02-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class VectorParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (vector e1 e2 ...).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["vector", e1, e2, ...].
        """
        return scheme_parse(source)

    def test_vector_one_element(self):
        """
        Test (vector 1).
        """
        self.assertEqual(self._parse("(vector 1)"), ["vector", 1])

    def test_vector_two_elements(self):
        """
        Test (vector 1 #t).
        """
        self.assertEqual(self._parse("(vector 1 #t)"), ["vector", 1, True])

    def test_vector_three_elements(self):
        """
        Test (vector 1 #f ()).
        """
        self.assertEqual(self._parse("(vector 1 #f ())"), ["vector", 1, False, []])

    def test_vector_zero_elements(self):
        """
        Test (vector).
        """
        self.assertEqual(self._parse("(vector)"), ["vector"])

if __name__ == '__main__':
    unittest.main()
