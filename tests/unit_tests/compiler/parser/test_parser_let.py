# test_parser_let.py - tests (let bindings body)  parsing
#
# Josh Meise
# 02-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LetParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of (let bindings body).
    """

    def _parse(self, source: str) -> list:
        """
        Parses the provided Scheme source code.
        Wrapper around Parser class' parse() function.

        Args:
            source (str): Scheme source code to be parsed.

        Returns:
            list: ["let", bindings, body]
        """
        return scheme_parse(source)

    def test_let_one_binding_unused(self):
        """
        Test (let ((a 4)) 3).
        """
        self.assertEqual(self._parse("(let ((a 4)) 3)"), ["let", [4], [3]])
    
    def test_let_one_binding_used(self):
        """
        Test (let ((a 4)) a).
        """
        self.assertEqual(self._parse("(let ((a 4)) a)"), ["let", [4], ["b0"]])

    def test_let_two_bindings_first_used(self):
        """
        Test (let ((a 4) (b 5)) a).
        """
        self.assertEqual(self._parse("(let ((c 4) (b 5)) c)"), ["let", [4, 5], ["b0"]])

    def test_let_two_bindings_second_used(self):
        """
        Test (let ((a 4) (b 5)) b).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) b)"), ["let", [4, 5], ["b1"]])

    def test_let_two_bindings_both_used(self):
        """
        Test (let ((a 4) (b 5)) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) (+ a b))"), ["let", [4, 5], [["+", "b0", "b1"]]])

    def test_let_two_bindings_both_used_expr_in_one(self):
        """
        Test (let ((a 4) (b (+ 3 4))) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a 4) (b (+ 3 4))) (+ a b))"), ["let", [4, ["+", 3, 4]], [["+", "b0", "b1"]]])

    def test_let_bindings_invalid_id(self):
        """
        Test (let ((a 4) (#b (+ 3 4))) (+ a #b)).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(let ((a 4) (#b (+ 3 4))) (+ a #b))")

    def test_let_bindings_unbound_id(self):
        """
        Test (let ((a 4) (b (+ 3 4))) (+ a c)).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(let ((a 4) (b (+ 3 4))) (+ a c))")

    def test_let_nested_expr_body(self):
        """
        Test (let ((a (+ 4 5)) (b (- 3 1)) (c 134)) (+ a (+ b c))).
        """
        self.assertEqual(self._parse("(let ((a (+ 4 5)) (b (- 3 1)) (c 134)) (+ a (+ b c)))"), ["let", [["+", 4, 5], ["-", 3, 1], 134], [["+", "b0", ["+", "b1", "b2"]]]])

    def test_let_nested_binding_diff_name(self):
        """
        Test (let ((b (let ((a 4)) a))) b).
        """
        self.assertEqual(self._parse("(let ((b (let ((a 4)) a))) b)"), ["let", [["let", [4], ["b0"]]], ["b0"]])

    def test_let_nested_binding_same_name(self):
        """
        Test (let ((a (let ((a 4)) a))) a).
        """
        self.assertEqual(self._parse("(let ((a (let ((a 4)) a))) a)"), ["let", [["let", [4], ["b0"]]], ["b0"]])

    def test_let_nested_body_diff_name(self):
        """
        Test (let ((b 4)) (let ((a 5)) (+ a b))).
        """
        self.assertEqual(self._parse("(let ((b 4)) (let ((a 5)) (+ a b)))"), ["let", [4], [["let", [5], [["+", "b1", "b0"]]]]])

    def test_let_nested_body_same_name(self):
        """
        Test (let ((a 4)) (let ((a 5)) (+ a a))).
        """
        self.assertEqual(self._parse("(let ((a 4)) (let ((a 5)) (+ a a)))"), ["let", [4], [["let", [5], [["+", "b1", "b1"]]]]])

    def test_let_nested_body_two_bindings(self):
        """
        Test (let ((b 4) (c 3)) (let ((a 5)) (+ a (- b c)))).
        """
        self.assertEqual(self._parse("(let ((b 4) (c 3)) (let ((a 5)) (+ a (- b c))))"), ["let", [4, 3], [["let", [5], [["+", "b2", ["-", "b0", "b1"]]]]]])

    def test_let_nested_body_two_bindings_body(self):
        """
        Test (let ((b 4) (c 3)) (let ((a 5) (d 4)) (+ a (- (+ b d) c)))).
        """
        self.assertEqual(self._parse("(let ((b 4) (c 3)) (let ((a 5) (d 4)) (+ a (- (+ b d) c))))"), ["let", [4, 3], [["let", [5, 4], [["+", "b2", ["-", ["+", "b0", "b3"], "b1"]]]]]])

if __name__ == '__main__':
    unittest.main()
