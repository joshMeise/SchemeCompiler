# test_interpterer_is_bool.py - tests interpretation of boolean?
#
# Josh Meise
# 01-09-2026
# Description:
#
# Citations:
# - ChatGPT for subprocess with stdin and capturing stdout.
#

import unittest
import sys
import os
import subprocess

INTERPRETER_UTILS_DIR = "./interpreter/utils/"
INTERPRETER_EXECS_DIR = "./interpreter/execs/"
INTERPRET = "./interpreter/execs/interpret"

class IsBoolInterpreterTests(unittest.TestCase):
    """
    Unit testing framework for interpreting (boolean? e).
    """
    def _interpret(self, source: bytes) -> int:
        """
        Calls interpreter and interprets byte code.

        Args:
            source (bytes): Bytecode to be interpreted.

        Returns:
            int: Integer value output by interpreter.
        """
        inter = subprocess.Popen([INTERPRET], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

        stdout, stderr = inter.communicate(source)

        return stdout.decode("utf-8")

    def test_is_boolean_true(self):
        """
        Test (boolean? #t).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x9F\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#t\n")

    def test_is_boolean_false(self):
        """
        Test (boolean? #f).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x1F\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#t\n")

    def test_is_boolean_a(self):
        """
        Test (boolean? #\a).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x0F\x61\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#f\n")

    def test_is_boolean_empty_list(self):
        """
        Test (boolean? ()).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x2F\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#f\n")

    def test_is_boolean_1(self):
        """
        Test (boolean? 1).
        """
        self.assertEqual(self._interpret(b"\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00"), "#f\n")

if __name__ == '__main__':
    unittest.main()
