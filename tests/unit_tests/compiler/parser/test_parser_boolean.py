# test_parser_boolean.py - tests boolean parsing
#
# Josh Meise
# 01-18-2026
# Description:
# - Tests parsing of true and fasle values.
#

import unittest
import sys
import os
from compiler.parser import Parser

class BooleanParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of booleans.
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
        return Parser(source).parse()

    def test_regular_true(self):
        """
        Test true value.
        """
        self.assertEqual(self._parse("#t"), True)

    def test_true_leading_whitespace(self):
        """
        Tests true value with leading whitespace.
        """
        self.assertEqual(self._parse("     #t"), True)

    def test_true_trailing_whitespace(self):
        """
        Tests true value with trailing whitespace.
        """
        self.assertEqual(self._parse("#t   "), True)

    def test_true_leading_trailing_whitespace(self):
        """
        Tests true with both leading and trailing whitespace.
        """
        self.assertEqual(self._parse("    #t   "), True)

    def test_uppercase_true(self):
        """
        Tests true with uppercase 'T'.
        """
        self.assertEqual(self._parse("#T"), True)

    def test_regular_false(self):
        """
        Test false value.
        """
        self.assertEqual(self._parse("#f"), False)

    def test_false_leading_whitespace(self):
        """
        Tests false value with leading whitespace.
        """
        self.assertEqual(self._parse("     #f"), False)

    def test_false_trailing_whitespace(self):
        """
        Tests false value with trailing whitespace.
        """
        self.assertEqual(self._parse("#f   "), False)

    def test_false_leading_trailing_whitespace(self):
        """
        Tests false with both leading and trailing whitespace.
        """
        self.assertEqual(self._parse("    #f   "), False)

    def test_uppercase_false(self):
        """
        Tests false with uppercase 'F'.
        """
        self.assertEqual(self._parse("#F"), False)

    def test_invalid_char(self):
        """
        Test pound sign followed by invalid character.
        """
        with self.assertRaises(TypeError):
            self._parse("#l")

    def test_invalid_string(self):
        """
        Test pound sign followed by ,ore than one character.
        """
        with self.assertRaises(TypeError):
            self._parse("#tf")

    def test_leading_char(self):
        """
        Test no leading pound sign.
        """
        with self.assertRaises(NotImplementedError):
            self._parse("tf")

if __name__ == '__main__':
    unittest.main()
