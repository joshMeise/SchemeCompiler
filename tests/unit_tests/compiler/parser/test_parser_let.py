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
        self.assertEqual(self._parse("(let ((a 4)) 3)"), ["let", [("a", 4)], 3])
    
    def test_let_one_binding_used(self):
        """
        Test (let ((a 4)) a).
        """
        self.assertEqual(self._parse("(let ((a 4)) a)"), ["let", [("a", 4)], Local("a")])

    def test_let_two_bindings_first_used(self):
        """
        Test (let ((a 4) (b 5)) a).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) a)"), ["let", [("a", 4), ("b", 5)], Local("a")])

    def test_let_two_bindings_second_used(self):
        """
        Test (let ((a 4) (b 5)) b).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) b)"), ["let", [("a", 4), ("b", 5)], Local("b")])

    def test_let_two_bindings_both_used(self):
        """
        Test (let ((a 4) (b 5)) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a 4) (b 5)) (+ a b))"), ["let", [("a", 4), ("b", 5)], ["+", Local("a"), Local("b")]])

    def test_let_two_bindings_both_used_expr_in_one(self):
        """
        Test (let ((a 4) (b (+ 3 4))) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a 4) (b (+ 3 4))) (+ a b))"), ["let", [("a", 4), ("b", ["+", 3, 4])], ["+", Local("a"), Local("b")]])

    def test_let_bindings_invalid_id(self):
        """
        Test (let ((a 4) (#b (+ 3 4))) (+ a #b)).
        """
        with self.assertRaises(RuntimeError):
            self._parse("(let ((a 4) (#b (+ 3 4))) (+ a #b))")

    def test_let_nested_expr_body(self):
        """
        Test (let ((a (+ 4 5)) (b (- 3 1)) (c 134)) (+ a (+ b c))).
        """
        self.assertEqual(self._parse("(let ((a (+ 4 5)) (b (- 3 1)) (c 134)) (+ a (+ b c)))"), ["let", [("a", ["+", 4, 5]), ("b", ["-", 3, 1]), ("c", 134)], ["+", Local("a"), ["+", Local("b"), Local("c")]]])

    def test_let_nested_binding_diff_name(self):
        """
        Test (let ((b (let ((a 4)) a))) b).
        """
        self.assertEqual(self._parse("(let ((b (let ((a 4)) a))) b)"), ["let", [("b", ["let", [("a", 4)], Local("a")])], Local("b")])

    def test_let_nested_binding_same_name(self):
        """
        Test (let ((a (let ((a 4)) a))) a).
        """
        self.assertEqual(self._parse("(let ((a (let ((a 4)) a))) a)"), ["let", [("a", ["let", [("a", 4)], Local("a")])], Local("a")])

    def test_let_nested_body_diff_name(self):
        """
        Test (let ((b 4)) (let ((a 5)) (+ a b))).
        """
        self.assertEqual(self._parse("(let ((b 4)) (let ((a 5)) (+ a b)))"), ["let", [("b", 4)], ["let", [("a", 5)], ["+", Local("a"), Local("b")]]])

    def test_let_nested_body_same_name(self):
        """
        Test (let ((a 4)) (let ((a 5)) (+ a a))).
        """
        self.assertEqual(self._parse("(let ((a 4)) (let ((a 5)) (+ a a)))"), ["let", [("a", 4)], ["let", [("a", 5)], ["+", Local("a"), Local("a")]]])

    def test_let_nested_body_two_bindings(self):
        """
        Test (let ((b 4) (c 3)) (let ((a 5)) (+ a (- b c)))).
        """
        self.assertEqual(self._parse("(let ((b 4) (c 3)) (let ((a 5)) (+ a (- b c))))"), ["let", [("b", 4), ("c", 3)], ["let", [("a", 5)], ["+", Local("a"), ["-", Local("b"), Local("c")]]]])

    def test_let_nested_body_two_bindings_body(self):
        """
        Test (let ((b 4) (c 3)) (let ((a 5) (d 4)) (+ a (- (+ b d) c)))).
        """
        self.assertEqual(self._parse("(let ((b 4) (c 3)) (let ((a 5) (d 4)) (+ a (- (+ b d) c))))"), ["let", [("b", 4), ("c", 3)], ["let", [("a", 5), ("d", 4)], ["+", Local("a"), ["-", ["+", Local("b"), Local("d")], Local("c")]]]])

    def test_many_nested_1(self):
        """
        Test (let ((a 4)) (let ((a (let ((a 5)) a))) (let ((a 6)) a)))
        """
        self.assertEqual(self._parse("(let ((a 4)) (let ((a (let ((a 5)) a))) (let ((a 6)) a)))"), ['let', [('a', 4)], ['let', [('a', ['let', [('a', 5)], Local('a')])], ['let', [('a', 6)], Local('a')]]])

    def test_many_nested_2(self):
        """
        Test (let ((a (let ((a 5)) a))) (let ((a 6)) a))
        """
        self.assertEqual(self._parse("(let ((a (let ((a 5)) a))) (let ((a 6)) a))"), ['let', [('a', ['let', [('a', 5)], Local('a')])], ['let', [('a', 6)], Local('a')]])

    def test_missing_body(self):
        """
        Test (let ((a 4)))
        """
        with self.assertRaises(RuntimeError):
            self._parse("(let ((a 4)))")

    def test_unbound_1(self):
        """
        Test (let ((a 4)) (let ((a (let ((a 5)) b))) (let ((a 6)) a)))
        """
        self.assertEqual(self._parse("(let ((a 4)) (let ((a (let ((a 5)) b))) (let ((a 6)) a)))"), ['let', [('a', 4)], ['let', [('a', ['let', [('a', 5)], 'b'])], ['let', [('a', 6)], Local('a')]]])

    def test_unbound_2(self):
        """
        Test (let ((a 4)) (let ((b 4) (a (let ((a 5)) b))) (let ((a 6)) a)))
        """
        self.assertEqual(self._parse("(let ((a 4)) (let ((b 4) (a (let ((a 5)) b))) (let ((a 6)) a)))"), ['let', [('a', 4)], ['let', [('b', 4), ('a', ['let', [('a', 5)], 'b'])], ['let', [('a', 6)], Local('a')]]])


if __name__ == '__main__':
    unittest.main()
