# test_parser_labmda.py - tests lambda parsing
#
# Josh Meise
# 02-05-2026
# Description:
#

import unittest
import sys
import os
from compiler.parser import *

class LambdaParseTests(unittest.TestCase):
    """
    Unit testing framework for the parsing of lambda expressions.
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

    def test_lambda_one_bound(self):
        """
        Test (lambda (x) x).
        """
        self.assertEqual(self._parse("(lambda (x) x)"), ["labels", [("f0", ["code", ["x"], [], Bound("x")])], ["closure", "f0"]])

    def test_lambda_one_bound_one_free(self):
        """
        Test (lambda (y) (+ x y)).
        """
        self.assertEqual(self._parse("(lambda (y) (+ x y))"), ["labels", [("f0", ["code", ["y"], ["x"], ["+", Free("x"), Bound("y")]])], ["closure", "f0", "x"]])

    def test_lambda_one_free(self):
        """
        Test (let ((x 5)) (lambda () x)).
        """
        self.assertEqual(self._parse("(let ((x 5)) (lambda () x))"), ["labels", [("f1", ["code", [], ["x"], Free("x")])], ["let", [("x", 5)], ["closure", "f1", Local("x")]]])

    def test_lambda_one_free_called_1(self):
        """
        Test ((let ((x 5)) (lambda () x))).
        """
        self.assertEqual(self._parse("((let ((x 5)) (lambda () x)))"), ["labels", [("f2", ["code", [], ["x"], Free("x")])], [["let", [("x", 5)], ["closure", "f2", Local("x")]]]])

    def test_lambda_one_free_called_2(self):
        """
        Test (let ((x 5)) ((lambda () x))).
        """
        self.assertEqual(self._parse("(let ((x 5)) ((lambda () x)))"), ["labels", [("f2", ["code", [], ["x"], Free("x")])], ["let", [("x", 5)], [["closure", "f2", Local("x")]]]])

    def test_lambda_two_free(self):
        """
        Test (let ((x 5) (y 4)) (lambda () (+ x y))).
        """
        self.assertEqual(self._parse("(let ((x 5) (y 4)) (lambda () (+ x y)))"), ["labels", [("f2", ["code", [], ["x", "y"], ["+", Free("x"), Free("y")]])], ["let", [("x", 5), ("y", 4)], ["closure", "f2", Local("x"), Local("y")]]])

    def test_lambda_with_let_bound(self):
        """
        Test (let ((x 3)) (lambda (y) y)).
        """
        self.assertEqual(self._parse("(let ((x 3)) (lambda (y) y))"), ["labels", [("f1", ["code", ["y"], [], Bound("y")])], ["let", [("x", 3)], ["closure", "f1"]]])

    def test_lambda_called_no_arg(self):
        """
        Test ((lambda () 3)).
        """
        self.assertEqual(self._parse("((lambda () 3))"), ["labels", [("f1", ["code", [], [], 3])], [["closure", "f1"]]])

    def test_lambda_called_one_arg(self):
        """
        Test ((lambda (x) (+ x 3)) 4).
        """
        self.assertEqual(self._parse("((lambda (x) (+ x 3)) 4)"), ["labels", [("f0", ["code", ["x"], [], ["+", Bound("x"), 3]])], [["closure", "f0"], 4]])

    def test_lambda_two_bindings(self):
        """
        Test (let ((a ((lambda () 4))) (b ((lambda () 3)))) (+ a b)).
        """
        self.assertEqual(self._parse("(let ((a ((lambda () 4))) (b ((lambda () 3)))) (+ a b))"), ["labels", [("f1", ["code", [], [], 4]), ("f2", ["code", [], [], 3])], ['let', [('a', [['closure', 'f1']]), ('b', [['closure', 'f2']])], ['+', Local('a'), Local('b')]]])

    def test_lambda_two_bound_two_free(self):
        """
        Test (let ((a 5) (b 1)) (lambda (x y) (+ (- (- y x) b) a)))
        """
        self.assertEqual(self._parse("(let ((a 5) (b 1)) (lambda (x y) (+ (- (- y x) b) a)))"), ["labels", [("f2", ["code", ["x", "y"], ["b", "a"], ["+", ["-", ["-", Bound("y"), Bound("x")], Free("b")], Free("a")]])], ["let", [("a", 5), ("b", 1)], ["closure", "f2", Local("b"), Local("a")]]])

    def test_lambda_bound_in_let(self):
        """
        Test (let ((b 2)) (let ((a (lambda (y) (+ y b)))) (+ (a 1) (a 1))))
        """
        self.assertEqual(self._parse("(let ((b 2)) (let ((a (lambda (y) (+ y b)))) (+ (a 1) (a 1))))"), ["labels", [("f1", ["code", ["y"], ["b"], ["+", Bound("y"), Free("b")]])], ["let", [("b", 2)], ["let", [("a", ["closure", "f1", Local("b")])], ["+", [Local("a"), 1], [Local("a"), 1]]]]])

    def test_lambda_nested_uncalled(self):
        """
        Test (let ((x 5)) (lambda (y) (lambda () (+ x y)))).
        """
        self.assertEqual(self._parse("(let ((x 5)) (lambda (y) (lambda () (+ x y))))"), ["labels", [("f2", ["code", [], ["x", "y"], ["+", Free("x"), Free("y")]]), ("f1", ["code", ["y"], ["x"], ["closure", "f2", Free("x"), Bound("y")]])], ["let", [("x", 5)], ["closure", "f1", Local("x")]]])

    def test_lambda_nested_called(self):
        """
        Test (let ((x 5)) (((lambda (y) (lambda () (+ x y))) 3))).
        """
        self.assertEqual(self._parse("(let ((x 5)) (((lambda (y) (lambda () (+ x y))) 3)))"), ["labels", [("f3", ["code", [], ["x", "y"], ["+", Free("x"), Free("y")]]), ("f2", ["code", ["y"], ["x"], ["closure", "f3", Free("x"), Bound("y")]])], ["let", [("x", 5)], [[["closure", "f2", Local("x")], 3]]]])

    def test_lambda_as_arg(self):
        """
        Test ((lambda (x) x) ((lambda () 5))).
        """
        self.assertEqual(self._parse("((lambda (x) x) ((lambda () 5)))"), ["labels", [("f0", ["code", ["x"], [], Bound("x")]), ("f2", ["code", [], [], 5])], [["closure", "f0"], [["closure", "f2"]]]])

    def test_lambda_factorial_regular(self):
        """
        Test ((lambda (fact) (fact fact 5 1)) (lambda (self n acc) (if (= n 0) acc (self self (- n 1) (* acc n)))))
        """
        self.assertEqual(self._parse("((lambda (fact) (fact fact 5 1)) (lambda (self n acc) (if (= n 0) acc (self self (- n 1) (* acc n)))))"), ["labels", [("f0", ["code", ["fact"], [], [Bound("fact"), Bound("fact"), 5, 1]]), ("f1", ["code", ["self", "n", "acc"], [], ["if", ["=", Bound("n"), 0], Bound("acc"), [Bound("self"), Bound("self"), ["-", Bound("n"), 1], ["*", Bound("acc"), Bound("n")]]]])], [["closure", "f0"], ["closure", "f1"]]])


    def test_lambda_factorial_tail_called(self):
        """
        Test ((lambda (fact) (fact fact 5 1)) (lambda (self n acc) (if (= n 0) acc (self self (- n 1) (* acc n)))))
        """
        self.assertEqual(self._parse("((lambda (fact) (fact fact 5 1)) (lambda (self n acc) (if (= n 0) acc (self self (- n 1) (* acc n)))))"), ["labels", [("f0", ["code", ["fact"], [], [Bound("fact"), Bound("fact"), 5, 1]]), ("f1", ["code", ["self", "n", "acc"], [], ["if", ["=", Bound("n"), 0], Bound("acc"), [Bound("self"), Bound("self"), ["-", Bound("n"), 1], ["*", Bound("acc"), Bound("n")]]]])], [["closure", "f0"], ["closure", "f1"]]])


if __name__ == '__main__':
    unittest.main()
