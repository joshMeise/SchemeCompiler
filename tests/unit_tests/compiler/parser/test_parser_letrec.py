# test_parser_letrec.py - tests parsing of letrec
#
# Josh Meise
# 03-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LetrecParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of letrec.
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: closure form of lambda expression
        """
        return scheme_parse(source)

    #def test_letrec_simple(self):
        """
        Test (letrec ((a (lambda () (b))) (b (lambda () 4))) (+ (a) (b))).
        """
        #self.assertEqual(self._parse("(letrec ((a (lambda () (b))) (b (lambda () 4))) (+ (a) (b)))"), ["letrec", [("a", )

if __name__ == '__main__':
    unittest.main()
